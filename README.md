<p align="center">
  <a href="" rel="noopener">
 <img width=400px src="assets/img/title.png" alt="Project logo"></a>
</p>

<h1 align="center">AnaHiePro</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/danylevych/AnaHiePro/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/danylevych/AnaHiePro/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p> 
<b>AnaHiePro</b> is a module that allows solving various tasks of systems analysis using the Analytic Hierarchy Process (AHP).
    <br> 
</p>

## 📝 Content

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Authors](#authors)


## 🧐 About <a name = "about"></a>

<b>AnaHiePro</b>  is a Python module designed to simplify the decision-making process by using the Analytic Hierarchy Process (AHP) method. This method allows you to structure complex problems in the form of a hierarchical model consisting of goals, criteria, and alternatives. AnaHiePro automatically calculates global priorities for the entire hierarchy.

The module provides a recursive traversal of the hierarchical tree, starting from the leaf nodes and moving up to the root. Each level of the hierarchy is processed by multiplying the matrix of local child vectors by the global parent vector, which allows you to determine the weight of each element at all levels. This makes AnaHiePro an ideal tool for analyzing complex systems and making informed decisions in a variety of fields, including business, project management, scientific research, and more.

## 🏁 Getting Started <a name = "getting_started"></a>

<h4>This is simple instruction how to install <b>AnaHiePro</b> on your PC and start to use it.<h4>

### Installing

Open the terminal window and write the following command:

```
pip install anahiepro
```

After loading you can use all AnaHiePro's functionality, down below you can see the simplest way of using AnaHiePro.

```py
from anahiepro.nodes import Problem, Criteria, Alternative, DummyCriteria
from anahiepro.models.model import Model

problem = Problem("Example Problem")

list_of_criterias = [
    Criteria("Citeria_1"),
    Criteria("Citeria_2"),
    Criteria("Citeria_3")
]

alternatives = [
    Alternative("Alternative_1"),
    Alternative("Alternative_1")
]

model = Model(problem, list_of_criterias, alternatives)

print(model.show())
```


## 🎈 Usage <a name="usage"></a>




## ✍️ Authors <a name = "authors"></a>

- [@danylevych](https://github.com/danylevych) - Idea & Initial work
