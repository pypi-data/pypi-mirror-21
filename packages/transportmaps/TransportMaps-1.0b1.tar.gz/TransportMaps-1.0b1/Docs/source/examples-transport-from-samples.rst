Inverse transports from samples (density estimation)
====================================================

Here we discuss settings where one is **able to sample** the `distribution <api-TransportMaps-Distributions.html#TransportMaps.Distributions.Distribution>`_ :math:`\nu_\pi` (or is provided a finite number of samples) and wants to characterize its density :math:`\pi`. This kind of problems go under the name of **density estimation**. We then seek a transport map :math:`S:\mathbb{R}^d \rightarrow \mathbb{R}^d` that pushes forward the target density :math:`\pi` to an amenable reference density :math:`\rho`. This is achieved solving the following problem:

.. math::
   
   S^\star &= \arg\min_{S \in \mathcal{T}} \mathcal{D}_{\rm KL}\left( S_\sharp \pi \middle\Vert \rho \right) 
   = \arg\min_{S \in \mathcal{T}} \mathcal{D}_{\rm KL}\left( \pi \middle\Vert S^\sharp \rho \right) \\
   &= \arg\min_{S \in \mathcal{T}} \mathbb{E}_\pi \left[ \log \frac{\pi}{S^\sharp \rho} \right] 
   = \arg\min_{S \in \mathcal{T}} \mathbb{E}_\pi \left[ - \log S^\sharp \rho \right]

where the expectation with respect to :math:`\pi` can be approximated because we can sample (or we are given samples of) the distribution :math:`\nu_\pi`.

For more details on the topic we refer to the available literature :cite:`Parno2014`.

**Contents**

.. toctree::
   :maxdepth: 2

   example-inverse-gumbel-1d.ipynb
   example-inverse-stochastic-volatility-6d.ipynb

