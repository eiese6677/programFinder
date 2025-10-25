program_name = input("🔍 패키지 이름을 입력하세요: ").strip()
while not program_name:
    program_name = input("❗ 패키지 이름은 필수입니다.: ").strip()

# 출력 형식 선택
output_type = input("📤 출력 형식을 선택하세요 (print / file / all) [기본값: all]: ").strip().lower()
if output_type not in ("print", "file", "all"):
    output_type = "all"

# 파일 출력인 경우
output_name = "output.txt"
if output_type in ("file", "all"):
    name_input = input("💾 출력 파일 이름을 입력하세요 [기본값: output.txt]: ").strip()
    if name_input:
        output_name = name_input

# 탐색 루트 디렉터리 입력
root_input = input("📂 탐색할 디렉터리를 쉼표로 구분해 입력하세요 (예: /,/usr) [기본값: PATH]: ").strip()
root = root_input.split(",") if root_input else []

print("\n⚙️ 설정 요약")
print(f" - 패키지 이름: {program_name}")
print(f" - 출력 형식: {output_type}")
print(f" - 출력 파일: {output_name}")
print(f" - 탐색 경로: {root if root else 'PATH 환경변수 사용'}")
