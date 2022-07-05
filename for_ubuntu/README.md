```
git clone https://github.com/argosopentech/argos-translate.git
cd argos-translate
pip install -e .
```

```
pip install opencc-python-reimplemented
```
```
pyinstaller -F --paths /Users/peiyutsai/miniforge3/envs/ubuntu38/lib/python3.8/site-packages translator_argo.py
```
```
pip install streamlit
```

```
pip download \
    --only-binary=:all: \ # 只下载二进制package（即wheel或egg）
    --platform linux_x86_64 \ # 说明是linux 64位架构
    --python-version 38 \ # Python 3.8
    --implementation cp \ # cpython，一般都是这个
    --abi cp27mu
    -r requirements.txt
    -d libraries

```
### Reference
* https://skeptric.com/python-offline-translation/
