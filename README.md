# Quantum codes do not fix qubit independent errors

This notebook complements the homonymous article written by the authors, by proving several claims made in the article with the assistance of a symbolic calculus library for Python, as well as in wxMaxima.

## Table of Contents

1. Authors
2. Python Implementation
    1. Online visualization
    2. Local execution and editing
        1. Code download
        2. Installation
    3. Execution

---

## 1. Authors

- J. Lacalle (1), [jesus.glopezdelacalle@upm.es](mailto://jesus.glopezdelacalle@upm.es)

- L. M. Pozo-Coronado (1), [lm.pozo@upm.es](mailto://lm.pozo@upm.es)

- A. L. Fonseca de Oliveira (2), [fonseca@ort.edu.uy](mailto://fonseca@ort.edu.uy)

- R. Martin-Cuevas (3), [r.martin-cuevas@alumnos.upm.es](mailto://r.martin-cuevas@alumnos.upm.es)

<p>
    <ul style="font-size: 11px;">
        <li>(1) Dep. de Matemática Aplicada a las TIC, ETS de Ingeniería de Sistemas Informáticos, Universidad Politécnica de Madrid, C/ Alan Turing s/n, 28031, Madrid, Spain</li>
        <li>(2) Facultad de Ingeniería, Universidad ORT, Montevideo, Uruguay</li>
        <li>(3) Programa de Doctorado en Ciencias y Tecnologías de la Computación para Smart Cities, ETS de Ingeniería de Sistemas Informáticos, Universidad Politécnica de Madrid, C/ Alan Turing s/n, 28031, Madrid, Spain</li>
    </ul>
</p>

---

## 1. Python Implementation

This version of the code has been developed using [Python 3](https://www.python.org/). Additionally, it uses SymPy ([Official website](https://www.sympy.org/en/index.html), [GitHub repo](https://github.com/sympy/sympy)), a Python library for symbolic mathematics, to perform the calculations described in the article. It also uses Jupyter Notebook ([Official website](https://jupyter.org/), [GitHub repo](https://github.com/jupyter/notebook)) to shape the document that contains the code and make it more readable, attaching all associated explanations and references to the main article.

You may choose to just visualize this document online, or to download it in your system if you intend to run it locally, and/or edit it.

### 1.i. Online visualization (without installation)

The latest version of the implementation in Python can be seen from Jupyter's online tool for Notebook visualization and sharing, nbviewer:

[Notebook on Jupyter's nbviewer](https://nbviewer.jupyter.org/github/rafamartinc/quantum_codes_do_not_fix_qubit_independent_errors/blob/main/jupyter/main.ipynb)

The cache duration on nbviewer.jupyter.org is approximately 10 minutes. Therefore, if a commit to this repository has been done in the last 10 minutes, you may not be seeing the last version of the code. To invalidate the cache and force nbviewer to re-render a notebook page, append ```?flush_cache=true``` to the URL.


### 1.ii Local execution and editing

#### 1.ii.a Code download

You may get this software by downloading this repository in a ZIP compressed file, directly from [this link](https://github.com/rafamartinc/quantum_codes_do_not_fix_qubit_independent_errors/archive/main.zip), and extracting it in the folder of your choice. Alternatively, you may also use the following git command (after installing Git on your system: [Linux and Unix](https://git-scm.com/download/linux), [Git for Windows](https://gitforwindows.org/))

##### Using HTTPS:
```shell
git clone https://github.com/rafamartinc/quantum_codes_do_not_fix_qubit_independent_errors.git
```

##### Using SSH:
```shell
git clone git@github.com:rafamartinc/quantum_codes_do_not_fix_qubit_independent_errors.git
```


##### 1.ii.b Installation

Begin by making sure that [Python 3](https://www.python.org/) is installed in the system that you intend to use to run the code. After installing it, you may use the following command to install the specific libraries used by this repository, after placing your terminal in the same folder where the repository files are located.

```shell
pip install -r jupyter/requirements.txt
```

##### 1.ii.c Execution

After the installation has been completed, and from the same terminal, you may run either one of the following commands to initialize the notebook. Feel free to run and tweak the code.

```shell
python -m notebook jupyter/main.ipynb
```

```shell
jupyter notebook jupyter/main.ipynb
```

---