import subprocess

def format_section(title, content):
    border = "=" * 15 + f"  {title}  " + "=" * 15
    return f"{border}\n{content.strip() if content.strip() else '(결과 없음)'}\n"

def findPackage(program_name,output_type="all",outputfile_name="output.txt"):
    if outputfile_name == '': outputfile_name = False

    results = []

    # apt-get
    try:
        proc = subprocess.run(['dpkg', '-L', program_name], capture_output=True, text=True)
        results.append(format_section("apt-get", proc.stdout if proc.returncode == 0 else proc.stderr))
    except FileNotFoundError:
        results.append(format_section("apt-get", "dpkg 명령어를 찾을 수 없습니다."))

    # gem
    try:
        proc1 = subprocess.Popen(["gem", "environment"], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(["grep", program_name], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc1.stdout.close()
        output, error = proc2.communicate()
        if proc2.returncode == 0:
            results.append(format_section("gem", output))
        else:
            results.append(format_section("gem", "(일치하는 결과 없음)"))
    except FileNotFoundError:
        results.append(format_section("gem", "'gem' 또는 'grep' 명령어를 찾을 수 없습니다."))

    # rpm
    try:
        proc1 = subprocess.Popen(["rpm", "-qa"], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(["grep", program_name], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc1.stdout.close()
        output, error = proc2.communicate()
        if proc2.returncode == 0:
            results.append(format_section("rpm", output))
        else:
            results.append(format_section("rpm", "(일치하는 결과 없음)"))
    except FileNotFoundError:
        results.append(format_section("rpm", "'rpm' 또는 'grep' 명령어를 찾을 수 없습니다."))

    # yum
    try:
        proc = subprocess.run(['yum', 'list', 'installed', program_name], capture_output=True, text=True)
        results.append(format_section("yum", proc.stdout if proc.returncode == 0 else proc.stderr))
    except FileNotFoundError:
        results.append(format_section("yum", "'yum' 명령어를 찾을 수 없습니다."))

    output_text = "\n".join(results)
    if output_type == "file":
        with open(outputfile_name, "w", encoding="utf-8") as f:
            f.write(output_text)
    if output_type == "print":
        print(output_text)
    if output_type == "all":
        with open(outputfile_name, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(output_text)
