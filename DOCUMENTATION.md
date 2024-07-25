<!-- markdownlint-disable -->

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `akvmodel.py`






---

## <kbd>class</kbd> `AKV`
AKV is a class that instantiates AKV models. 



**Args:**
 
 - <b>`belief_state`</b> (list[list[float]]):  The initial belief state as a list. 
 - <b>`influence_graph`</b> (list[list[float]]):  The influence graph as a adjacency             list. 
 - <b>`update_function`</b> (Callable[[list[list[float]], list[list[float]]], list[list[float]]):              A function the gets a belief_state and an influence_graph and returns a             new belief_state. 



**Attributes:**
 
 - <b>`belief_state`</b> (list[list[float]]):  Current belief state. It's a list of             lists, each list whitin is a belief array corresponding to the i-th             outcome in the domain. 
 - <b>`influence_graph`</b> (list[list[float]]):  Adjacency list for the influence graph. 
 - <b>`a`</b> (int):  Number of agents. 
 - <b>`k`</b> (int):  Size of the domain of independent outcomes for a proposition. 
 - <b>`states`</b> (list[list[list[float]]]):  list of all belief states computed so far             using the update function. 

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    belief_state: list[list[float]],
    influence_graph: list[list[float]],
    update_function: Callable[[list[list[float]], list[list[float]]], list[list[float]]]
)
```






---

#### <kbd>property</kbd> domain_size

Get the domain size, i.e. the number of belief arrays within a belief state. 

The domain represents a set of independent propositions. 



**Returns:**
 
 - <b>`int`</b>:  The number of independent propositions. 

---

#### <kbd>property</kbd> number_of_agents

Get the number of agents. 



**Returns:**
 
 - <b>`int`</b>:  Number of agents. 



---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_polarization`

```python
get_polarization(
    k: int = 201,
    K: float = 1000,
    alpha: float = 1.6
) → list[list[float]]
```

Get Esteban-Ray polarization for all states in the history. 



**Args:**
 
 - <b>`k`</b> (int, optional):  Number of bins. Defaults to 201. 
 - <b>`K`</b> (float, optional):  Hyperparameter K of the Esteban-Ray measure. Defaults                 to 1000. 
 - <b>`alpha`</b> (float, optional):  Hyperparameter $lpha$ of the Esteban-Ray                 measure. Defaults to 1.6. 



**Returns:**
 
 - <b>`list[float]`</b>:  list of polarization values. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `update`

```python
update() → list[list[float]]
```

Update the model one, updates the current belief state and add the new belief state to the history of states. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  New belief state. 


---

## <kbd>class</kbd> `InfluenceGraphs`
Catalog of Influence Graphs in the literature. All functions are static. 




---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `circular`

```python
circular(num_agents: int, influence: float = 0.5) → list[list[float]]
```

Creates a circular influence graph. 

The circular influence graph $\mathcal{I}^{clique}$ represents a social network in which agents can be organized in a circle in such a way each agent is only influenced by its predecessor and only influences its successor. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`influence`</b> (float, optional):  Influence that an agent has on the next one.                 Defaults to 0.5. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `clique`

```python
clique(num_agents: int, influence: float = 1) → list[list[float]]
```

Creates a clique influence graph. 

The clique influence graph $\mathcal{I}^{clique}$ represents an idealized totally connected social network. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`influence`</b> (float, optional):  Influence that every agent has on each                 other. Defaults to 1. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `disconnected`

```python
disconnected(num_agents: int, influence: float = 0.5) → list[list[float]]
```

Creates a disconnected influence graph. 

The disconnected influence graph $\mathcal{I}^{disc}$ represents a social network sharply divided into two groups in such a way that agents with the same group can considerably influence each other, just not all agents in the other group. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`influence`</b> (float, optional):  Influence between agents of the same                 group. Defaults to 0.5. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `faintly`

```python
faintly(
    num_agents: int,
    strong_influence: float = 0.5,
    weak_influence: float = 0.1
) → list[list[float]]
```

Creates a faintly communicating influence graph. 

The faintly communicating influence graph $\mathcal{I}^{faint}$ represents a social network divided into two groups that evolve mostly separately, with only faint communication between them. More precisely, agents from within the same group influence each other much more strongly than from different groups. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`strong_influence`</b> (float, optional):  Influence between agents of the same                 group. Defaults to 0.5. 
 - <b>`weak_influence`</b> (float, optional):  Influence between agents from different                 groups. Defaults to 0.1. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `malleable_influencers`

```python
malleable_influencers(
    num_agents: int,
    influencer_1_influence: float = 0.8,
    influencer_2_influence: float = 0.4,
    influence_on_influencer_1: float = 0.1,
    influence_on_influencer_2: float = 0.1,
    other_agents_influence: float = 0.1
) → list[list[float]]
```

Creates a malleable influencers influence graph. 

The malleable influencers influence graph $\mathcal{I}^{malleable}$ represents a social network in which two agents have a strong influence on every other agent, but are barely influenced by anyone else. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`influencer_1_influence`</b> (float, optional):  Influence that agent 0 has on                 other agents. Defaults to 0.8. 
 - <b>`influencer_2_influence`</b> (float, optional):  Influence that agents n - 1 has                 on other agents. Defaults to 0.4. 
 - <b>`influence_on_influencer_1`</b> (float, optional):  Influence that other agents                 have on agent 0. Defaults to 0.1. 
 - <b>`influence_on_influencer_2`</b> (float, optional):  Influence that other agents                 have on agent n - 1. Defaults to 0.1. 
 - <b>`other_agents_influence`</b> (float, optional):  Influence that the other agents                 have on each other. Defaults to 0.1. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L313"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `unrelenting_influencers`

```python
unrelenting_influencers(
    num_agents: int,
    influencer_1_influence: float = 0.6,
    influencer_2_influence: float = 0.6,
    other_agents_influence: float = 0.1
) → list[list[float]]
```

Creates an unrelenting influencers influence graph. 

The unrelenting influencers influence graph $\mathcal{I}^{unrel}$ represents a scenario in which two agents (say, $0$ and $n - 1$) exert a significantly stronger influence on every other agent than those other agents have among themselves. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 
 - <b>`influencer_1_influence`</b> (float, optional):  Influence that agent 0 has on                 other agents. Defaults to 0.6. 
 - <b>`influencer_2_influence`</b> (float, optional):  Influence that agents n - 1 has                 on other agents. Defaults to 0.6. 
 - <b>`other_agents_influence`</b> (float, optional):  Influence that the other agents                 have on each other. Defaults to 0.1. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Adjacency matrix for the influence graph. 


---

## <kbd>class</kbd> `InitialConfigurations`
Catalog of initial belief configurations in the literature. 




---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L401"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `extreme`

```python
extreme(num_agents: int) → list[list[float]]
```

Creates an extremely polarized belief configuration with domain of size 2. 

The extremely polarized belief configuration represents a situation in which half of the agents strongly believe the proposition, whereas half strongly disbelief it. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state for the inicial configuration. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `mildly`

```python
mildly(num_agents: int) → list[list[float]]
```

Creates a mildly polarized belief configuration with domain of size 2. 

The mildly polarized belief configuration with agents evenly split into two groups with moderately dissimilar inter-group belief compared to intra-groups beliefs 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state for the inicial configuration. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L428"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tripolar`

```python
tripolar(num_agents: int) → list[list[float]]
```

Creates an tripolar belief configuration with domain of size 2. 

The tripolar belief configuration with agents divided into three groups. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state for the inicial configuration. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L352"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `uniform`

```python
uniform(num_agents: int) → list[list[float]]
```

Creates a uniform belief configuration with domain of size 2. 

The uniform belief configuration represents a set of agents whose beliefs are as varied as possible, all equally spaced in the interval $[0, 1]$. 



**Args:**
 
 - <b>`num_agents`</b> (int):  Number of agents. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state for the inicial configuration. 


---

## <kbd>class</kbd> `UpdateFunctions`
Catalog of update functions in the literature. All functions are static. 




---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `classic`

```python
classic(
    belief_state: list[list[float]],
    influence_graph: list[list[float]]
) → list[list[float]]
```

Computes the classic update of a belief state given a influence graph. 



**Args:**
 
 - <b>`belief_state`</b> (list[list[float]]):  Belief state at time $t$. 
 - <b>`influence_graph`</b> (list[list[float]]):  Influence graph as a adjacency matrix. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state at time $t + 1$. 

---

<a href="https://github.com/josecoliveira/akvmodel/tree/v1.2.2\akvmodel.py#L491"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `confirmation_bias`

```python
confirmation_bias(
    belief_state: list[list[float]],
    influence_graph: list[list[float]]
) → list[list[float]]
```

Computes the confirmation bias update of a belief state given a influence graph. 



**Args:**
 
 - <b>`belief_state`</b> (list[list[float]]):  Belief state at time $t$. 
 - <b>`influence_graph`</b> (list[list[float]]):  Influence graph as a adjacency matrix. 



**Returns:**
 
 - <b>`list[list[float]]`</b>:  Belief state at time $t + 1$. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
