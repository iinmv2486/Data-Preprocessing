import tiktoken

def split_text_by_tokens(input_file_path, output_folder_path, max_tokens=1000):
    """
    텍스트 파일을 주어진 최대 토큰 수를 기준으로 분할하여 여러 파일로 저장합니다.

    :param input_file_path: 분할할 텍스트 파일 경로
    :param output_folder_path: 분할된 파일을 저장할 폴더 경로
    :param max_tokens: 각 파일에 포함할 최대 토큰 수
    """
    # tiktoken을 사용하여 OpenAI의 GPT-4 모델용 토크나이저 불러오기
    tokenizer = tiktoken.encoding_for_model("gpt-4o")

    # 텍스트 파일 읽기
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 텍스트를 토큰화
    tokens = tokenizer.encode(text)
    
    # 텍스트를 토큰 수에 맞게 분할
    parts = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]

    # 분할된 텍스트 저장
    for idx, part in enumerate(parts):
        part_text = tokenizer.decode(part)
        part_file_path = f"{output_folder_path}/part_{idx + 1}.txt"
        with open(part_file_path, 'w', encoding='utf-8') as part_file:
            part_file.write(part_text)

    print(f"총 {len(parts)}개의 파일로 분할되었습니다.")

# 사용 예시
input_file_path = '/home/user/문서/GitHub/Data Preprocessing/youtube_scripts/Complete Generative AI With Azure Cloud Open AI Services Crash Course - English.txt'
output_folder_path = '/home/user/문서/GitHub/Hugging-Face-Models/Data Preprocessing/result data'
split_text_by_tokens(input_file_path, output_folder_path, max_tokens=1000)
