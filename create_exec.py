# 导入QPT
from qpt.executor import CreateExecutableModule as CEM
from qpt.modules.package import CopyWhl2Packages

# TODO: Add ENV Path variables                                                       
module = CEM(work_dir="C:\\Users\\hkhalid\\Desktop\\ronicom-systems", 
             launcher_py_path="C:\\Users\\hkhalid\Desktop\\ronicom-systems\\main.py", 
             save_path="./outv1",
             sub_modules=[
                CopyWhl2Packages('C:\\Users\hkhalid\\Desktop\\ronicom-systems\\wheels2\\torch-1.13.1+cu116-cp39-cp39-win_amd64.whl'),
                CopyWhl2Packages('C:\\Users\hkhalid\\Desktop\\ronicom-systems\\wheels2\\torchaudio-0.13.1+cpu-cp39-cp39-win_amd64.whl'),
                CopyWhl2Packages('C:\\Users\hkhalid\\Desktop\\ronicom-systems\\wheels2\\torchvision-0.14.1+cu116-cp39-cp39-win_amd64.whl'),
            ],                         
             requirements_file="./requirements_with_opt.txt")                    
           # hidden_terminal=False                         
           # interpreter_module=Python37()               
                                                         
           # icon="your_ico.ico"                      
# 开始打包
module.make()