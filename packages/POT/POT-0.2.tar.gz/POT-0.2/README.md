# POT: Python Optimal Transport

[![PyPI version](https://badge.fury.io/py/POT.svg)](https://badge.fury.io/py/POT)
[![Build Status](https://travis-ci.org/rflamary/POT.svg?branch=master)](https://travis-ci.org/rflamary/POT)
[![Documentation Status](https://readthedocs.org/projects/pot/badge/?version=latest)](http://pot.readthedocs.io/en/latest/?badge=latest)


This open source Python library provide several solvers for optimization problems related to Optimal Transport for signal, image processing and machine learning.

It provides the following solvers:

* OT solver for the linear program/ Earth Movers Distance [1].
* Entropic regularization OT solver with Sinkhorn Knopp Algorithm [2] and stabilized version [9][10].
* Bregman projections for Wasserstein barycenter [3] and unmixing [4].
* Optimal transport for domain adaptation with group lasso regularization [5]
* Conditional gradient [6] and Generalized conditional gradient for regularized OT [7].
* Joint OT matrix and mapping estimation [8].
* Wasserstein Discriminant Analysis [11] (requires autograd + pymanopt).


Some demonstrations (both in Python and Jupyter Notebook format) are available in the examples folder.

## Installation

The Library has been tested on Linux and MacOSX. It requires a C++ compiler for using the EMD solver and rely on the following Python modules:

- Numpy (>=1.11)
- Scipy (>=0.17)
- Cython (>=0.23)
- Matplotlib (>=1.5)


Under debian based linux the dependencies can be installed with
```
sudo apt-get install python-numpy python-scipy python-matplotlib cython
```

To install the library, you can install it locally (after downloading it) on you machine using
```
python setup.py install --user
```

The toolbox is also available on PyPI with a possibly slightly older version. You can install it with:
```
pip install POT
```

After a correct installation, you should be able to import the module without errors:
```python
import ot
```

Note that for easier access the module is name ot instead of pot.

## Examples

The examples folder contain several examples and use case for the library. The full documentation is available on [Readthedocs](http://pot.readthedocs.io/)

 Here is a list of the Python notebooks if you want a quick look:

* [1D optimal transport](https://github.com/rflamary/POT/blob/master/examples/Demo_1D_OT.ipynb)
* [2D optimal transport on empirical distributions](https://github.com/rflamary/POT/blob/master/examples/Demo_2D_OT_samples.ipynb)
* [1D Wasserstein barycenter](https://github.com/rflamary/POT/blob/master/examples/Demo_1D_barycenter.ipynb)
* [OT with user provided regularization](https://github.com/rflamary/POT/blob/master/examples/Demo_Optim_OTreg.ipynb)
* [Domain adaptation with optimal transport](https://github.com/rflamary/POT/blob/master/examples/Demo_2D_OT_DomainAdaptation.ipynb)
* [Color transfer in images](https://github.com/rflamary/POT/blob/master/examples/Demo_Image_ColorAdaptation.ipynb)
* [OT mapping estimation for domain adaptation](https://github.com/rflamary/POT/blob/master/examples/Demo_2D_OTmapping_DomainAdaptation.ipynb)
* [OT mapping estimation for color transfer in images](https://github.com/rflamary/POT/blob/master/examples/Demo_Image_ColorAdaptation_mapping.ipynb)


You can also see the notebooks with [Jupyter nbviewer](https://nbviewer.jupyter.org/github/rflamary/POT/tree/master/examples/).

## Acknowledgements

The contributors to this library are:

* [Rémi Flamary](http://remi.flamary.com/)
* [Nicolas Courty](http://people.irisa.fr/Nicolas.Courty/)
* [Laetitia Chapel](http://people.irisa.fr/Laetitia.Chapel/)
* [Michael Perrot](http://perso.univ-st-etienne.fr/pem82055/)

This toolbox benefit a lot from open source research and we would like to thank the following persons for providing some code (in various languages):

* [Gabriel Peyré](http://gpeyre.github.io/) (Wasserstein Barycenters in Matlab)
* [Nicolas Bonneel](http://liris.cnrs.fr/~nbonneel/) ( C++ code for EMD)
* [Antoine Rolet](https://arolet.github.io/) ( Mex file for EMD )
* [Marco Cuturi](http://marcocuturi.net/) (Sinkhorn Knopp in Matlab/Cuda)

## References

[1] Bonneel, N., Van De Panne, M., Paris, S., & Heidrich, W. (2011, December). Displacement interpolation using Lagrangian mass transport. In ACM Transactions on Graphics (TOG) (Vol. 30, No. 6, p. 158). ACM.

[2] Cuturi, M. (2013). Sinkhorn distances: Lightspeed computation of optimal transport. In Advances in Neural Information Processing Systems (pp. 2292-2300).

[3] Benamou, J. D., Carlier, G., Cuturi, M., Nenna, L., & Peyré, G. (2015). Iterative Bregman projections for regularized transportation problems. SIAM Journal on Scientific Computing, 37(2), A1111-A1138.

[4] S. Nakhostin, N. Courty, R. Flamary, D. Tuia, T. Corpetti, Supervised planetary unmixing with optimal transport, Whorkshop on Hyperspectral Image and Signal Processing : Evolution in Remote Sensing (WHISPERS), 2016.

[5] N. Courty; R. Flamary; D. Tuia; A. Rakotomamonjy, "Optimal Transport for Domain Adaptation," in IEEE Transactions on Pattern Analysis and Machine Intelligence , vol.PP, no.99, pp.1-1

[6] Ferradans, S., Papadakis, N., Peyré, G., & Aujol, J. F. (2014). Regularized discrete optimal transport. SIAM Journal on Imaging Sciences, 7(3), 1853-1882.

[7] Rakotomamonjy, A., Flamary, R., & Courty, N. (2015). Generalized conditional gradient: analysis of convergence and applications. arXiv preprint arXiv:1510.06567.

[8] M. Perrot, N. Courty, R. Flamary, A. Habrard, "Mapping estimation for discrete optimal transport", Neural Information Processing Systems (NIPS), 2016.

[9] Schmitzer, B. (2016). Stabilized Sparse Scaling Algorithms for Entropy Regularized Transport Problems. arXiv preprint arXiv:1610.06519.

[10] Chizat, L., Peyré, G., Schmitzer, B., & Vialard, F. X. (2016). Scaling algorithms for unbalanced transport problems. arXiv preprint arXiv:1607.05816.

[11] Flamary, R., Cuturi, M., Courty, N., & Rakotomamonjy, A. (2016). Wasserstein Discriminant Analysis. arXiv preprint arXiv:1608.08063.