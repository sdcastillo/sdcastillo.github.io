---
layout: post
title:  "Using Jupyter Notebooks to Create Blog Posts"
date:   2017-10-10 12:07:25 +0000
categories:
  - development testing
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

This is a test post about creating blog posts easily using Jupyter.

## Code

```python
class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1],4) 
        self.weights2   = np.random.rand(4,1)                 
        self.y          = y
        self.output     = np.zeros(self.y.shape)
```

## Markdown Tables

| Column | Value |
|--------|-------|
| a      | 1     |
| b      | 2     | 
| c      | 3     |

## Latex

$$\text{Latex Test}$$
$$e^{i\pi} = -1$$



