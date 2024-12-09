# Jupyter notebook

Автоматическая конвертация main.py в main.ipynb вместе с ячейками вывода:

```bash
python -m jupytext --set-kernel python3 --to notebook --execute app.py
```
