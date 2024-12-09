# Jupyter notebook

## Автоматическая конвертация main.py в main.ipynb вместе с ячейками вывода:

```bash
python -m jupytext --set-kernel python3 --to notebook --execute app.py
```

## Ячейки с кодом в скрипте

VSCode как и некоторые другие IDE (PyCharm, Spyder) [поддерживает](https://code.visualstudio.com/docs/python/jupyter-support-py#_jupyter-code-cells) синтаксис [ячеек](https://jupytext.readthedocs.io/en/latest/formats-scripts.html) в python-скрипте. Таким образом можно получить плюсы как скрипта (полноценное версионирование в git), так и интерактивность Jupyter notebook.
