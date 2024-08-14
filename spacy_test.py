import spacy
from spacy.language import Language
import multiprocessing
import os
import logging
from tqdm import tqdm

# 로깅 설정
logging.basicConfig(filename='text_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 영어 언어 모델 로드
nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])

# 문장 경계 감지를 위한 커스텀 컴포넌트
@Language.component("custom_sbd")
def custom_sentence_boundary_detection(doc):
    for i, token in enumerate(doc[:-1]):
        doc[i+1].is_sent_start = False
        if (token.text.lower() not in ["and", "but", "or", "because", "since", "so"] and
            token.pos_ not in ["ADP", "PART", "CCONJ", "SCONJ"] and
            not token.is_punct and
            not token.is_currency and
            not doc[i+1].is_currency and
            not token.like_num and
            not doc[i+1].like_num and
            not token.is_quote and
            not doc[i+1].is_quote and
            token.pos_ != "PROPN" and
            doc[i+1].pos_ != "PROPN"):
            
            if (token.is_alpha and doc[i+1].is_alpha and 
                token.text.istitle() and not doc[i+1].text.istitle() and
                i > 0 and doc[i-1].text.lower() not in ["mr", "ms", "mrs", "dr", "prof"]):
                doc[i+1].is_sent_start = True
            elif (token.pos_ == "VERB" and doc[i+1].pos_ in ["NOUN", "PRON"] and
                  not any(child.dep_ in ["prep", "dobj", "pobj"] for child in token.children) and
                  i > 0 and doc[i-1].pos_ != "AUX"):
                doc[i+1].is_sent_start = True
    
    doc[0].is_sent_start = True
    return doc

# 커스텀 컴포넌트를 파이프라인에 추가
nlp.add_pipe("custom_sbd", before="parser")

def process_chunk(chunk):
    try:
        doc = nlp(chunk)
        sentences = list(doc.sents)
        processed_text = ""
        for sent in sentences:
            sentence_text = sent.text.strip() + "."
            sentence_text = sentence_text[0].upper() + sentence_text[1:]
            processed_text += sentence_text + " "
        return processed_text.strip()
    except Exception as e:
        logging.error(f"청크 처리 중 오류 발생: {e}")
        return None

def process_file(input_file, output_file, chunk_size=1000):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        chunk = ""
        words = 0
        chunks = []

        for line in f_in:
            chunk += line
            words += len(line.split())
            if words >= chunk_size:
                chunks.append(chunk)
                chunk = ""
                words = 0

        if chunk:  # 남은 텍스트 추가
            chunks.append(chunk)

        # 청크를 병렬로 처리
        with multiprocessing.Pool() as pool:
            results = list(tqdm(pool.imap(process_chunk, chunks), total=len(chunks), desc="청크 처리 중"))

        # 결과를 출력 파일에 쓰기
        for result in results:
            if result:
                f_out.write(result + "\n")
            else:
                logging.warning("처리 오류로 인해 None 결과가 발생했습니다.")

if __name__ == "__main__":
    input_file = "./youtube_scripts/Complete Generative AI With Azure Cloud Open AI Services Crash Course - English.txt"  # 입력 파일 경로로 교체
    output_file = "./Processed_data/Azure_script/result.txt"  # 원하는 출력 파일 경로로 교체

    if not os.path.exists(input_file):
        logging.error(f"입력 파일을 찾을 수 없습니다: {input_file}")
    else:
        logging.info(f"파일 처리 시작: {input_file}")
        process_file(input_file, output_file)
        logging.info(f"파일 처리 완료. 출력 파일: {output_file}")
