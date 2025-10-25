import FindPackage as fp
import findInPath as fip
import re

program_name = input("패키지 이름을 입력하세요: ").strip()
output_type = input("출력 형식을 입력하세요.(print,file,all(default)): ")
if not output_type.strip(): output_type = "all"
if output_type == 'file' or output_type == 'all':
    output_name = input("출력할 파일의 이름을 입력하세요.(생략 시 output.txt): ")
root = input("루트 디렉토리 선택 (예 : /,/usr)(생략 가능): ").split(",")
if output_name == '': output_name = "output.txt"
fp.findPackage(program_name, output_type=output_type, outputfile_name=output_name)
fip.search_program(program_name, root, output_type=output_type, outputfile_name=output_name)
