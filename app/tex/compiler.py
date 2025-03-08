
import io

import requests
import tarfile
from latex import build_pdf


def use_local_latex_compiler(tex_code: str, path: str) -> None:
    pdf = build_pdf(tex_code)
    pdf.save_to(path)


def use_remote_latex_compiler(remote_latex: str, tex_code: str, path: str) -> None:
    # write tex code to main.tex inside a tar file
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        texfile = io.BytesIO(tex_code.encode('utf-8'))
        tarinfo = tarfile.TarInfo(name='main.tex')
        tarinfo.size = len(tex_code.encode('utf-8'))
        tar.addfile(tarinfo, fileobj=texfile)
    tar_buffer.seek(0)
    
    # post tar file to latex compiler
    url = f'{remote_latex}/data?target=main.tex'
    files = { 'file': ('archive.tar', tar_buffer, 'application/x-tar') }
    ret = requests.post(url, files=files)

    # handle response
    if ret.status_code != 200:
        raise RuntimeError(ret.text)

    with open(path, 'wb') as file:
        file.write(ret.content)
    

def compile_pdf(remote_latex: str, tex_code: str, path: str) -> None:
    if remote_latex == '':
        use_local_latex_compiler(tex_code, path)
    else:
        use_remote_latex_compiler(remote_latex, tex_code, path)
