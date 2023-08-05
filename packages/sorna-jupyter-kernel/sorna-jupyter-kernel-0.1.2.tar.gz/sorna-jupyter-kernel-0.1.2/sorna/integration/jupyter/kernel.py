from ipykernel.kernelbase import Kernel as KernelBase
from sorna.kernel import Kernel
from sorna.exceptions import SornaAPIError


class SornaKernelBase(KernelBase):

    # ref: https://github.com/ipython/ipykernel/blob/master/ipykernel/kernelbase.py

    implementation = 'Sorna'
    implementation_version = '1.0'
    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Sorna (base)',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
    }
    banner = 'Sorna (base)'

    sorna_lang = 'python3'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug(f'__init__: {self.ident}')
        self.kernel = Kernel.get_or_create(self.sorna_lang, self.ident)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.log.debug('do_execute')
        self._allow_stdin = allow_stdin
        while True:
            result = self.kernel.execute(code, mode='query')

            if not silent:
                for item in result['console']:
                    if item[0] == 'stdout':
                        self.send_response(self.iopub_socket, 'stream', {
                            'name': 'stdout',
                            'text': item[1],
                        })
                    elif item[0] == 'stderr':
                        self.send_response(self.iopub_socket, 'stream', {
                            'name': 'stderr',
                            'text': item[1],
                        })
                    elif item[0] == 'media':
                        self.send_response(self.iopub_socket, 'display_data', {
                            'source': '<user-code>',
                            'data': { item[1][0]: item[1][1] },
                        })
                    elif item[0] == 'html':
                        self.send_response(self.iopub_socket, 'display_data', {
                            'source': '<user-code>',
                            'data': { 'text/html': item[1] },
                        })

            if result['status'] == 'finished':
                break
            elif result['status'] == 'waiting-input':
                if allow_stdin:
                    code = self.raw_input('')
                else:
                    code = '(user input not allowed)'
            elif result['status'] == 'continued':
                code = ''

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart=False):
        self.log.debug('do_shutdown')
        if restart:
            self.kernel.restart()
        else:
            try:
                self.kernel.destroy()
            except SornaAPIError as e:
                if e.args[0] == 404:
                    pass
                else:
                    self.log.exception()
            except:
                self.log.exception()


class SornaPythonKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Python 3 on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (Python 3)'

    sorna_lang = 'python3'


class SornaPythonTensorFlowKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, CPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-tensorflow'


class SornaPythonTorchKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, CPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-torch'


class SornaPythonTorchGPUKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, GPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-torch-gpu'


class SornaPythonTensorFlowGPUKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, GPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (GPU-accelerated TensorFlow with Python 3)'

    sorna_lang = 'python3-tensorflow-gpu'


class SornaJavascriptKernel(SornaKernelBase):

    language = 'javascript'
    language_version = '6'
    language_info = {
        'name': 'Javascript (NodeJS 6) on Sorna',
        'mimetype': 'text/javascript',
        'file_extension': '.js',
        'codemirror_mode': 'javascript',
    }
    banner = 'Sorna (NodeJS 6)'

    sorna_lang = 'nodejs6'


class SornaPHPKernel(SornaKernelBase):

    language = 'php'
    language_version = '7'
    language_info = {
        'name': 'PHP 7 on Sorna',
        'mimetype': 'text/x-php',
        'file_extension': '.php',
        'codemirror_mode': 'php',
    }
    banner = 'Sorna (PHP 7)'

    sorna_lang = 'php7'


class SornaJuliaKernel(SornaKernelBase):

    language = 'julia'
    language_version = '0.5'
    language_info = {
        'name': 'Julia 0.5 on Sorna',
        'mimetype': 'text/x-julia',
        'file_extension': '.jl',
        'codemirror_mode': 'julia',
    }
    banner = 'Sorna (Julia 0.5)'

    sorna_lang = 'julia'


class SornaRKernel(SornaKernelBase):

    language = 'r'
    language_version = '3'
    language_info = {
        'name': 'R 3 on Sorna',
        'mimetype': 'text/x-r-source',
        'file_extension': '.R',
        'codemirror_mode': 'Rscript',
    }
    banner = 'Sorna (R 3)'

    sorna_lang = 'r3'


class SornaLuaKernel(SornaKernelBase):

    language = 'lua'
    language_version = '5.3'
    language_info = {
        'name': 'Lua 5.3 on Sorna',
        'mimetype': 'text/x-lua',
        'file_extension': '.lua',
        'codemirror_mode': 'lua',
    }
    banner = 'Sorna (Lua 5.3)'

    sorna_lang = 'lua5'


sorna_kernels = [
    SornaPythonKernel,
    SornaPythonTorchKernel,
    SornaPythonTorchGPUKernel,
    SornaPythonTensorFlowKernel,
    SornaPythonTensorFlowGPUKernel,
    SornaJavascriptKernel,
    SornaPHPKernel,
    SornaJuliaKernel,
    SornaRKernel,
    SornaLuaKernel,
]
