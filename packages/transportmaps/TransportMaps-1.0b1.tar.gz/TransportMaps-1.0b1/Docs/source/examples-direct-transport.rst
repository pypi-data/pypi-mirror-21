Direct transports from densities (inference)
============================================

These examples treat the setting where one is **able to evaluate the un-normalized density** :math:`\pi` of a `distribution <api-TransportMaps-Distributions.html#TransportMaps.Distributions.Distribution>`_ :math:`\nu_{\pi}`, but its **sampling is hard**. A transport map :math:`T:\mathbb{R}^d \rightarrow \mathbb{R}^d` that pushes forward a reference density :math:`\rho` of a reference distribution :math:`\nu_\rho` to :math:`\pi` is constructed through the solution of the following optimization problem:

.. math::
   
   T^\star = \arg \min_{T \in \mathcal{T}} \mathcal{D}_{\rm KL}\left( T_\sharp \rho \Vert \pi\right)

For more details on the method we refer to the available literature :cite:`ElMoselhy2012`, :cite:`Marzouk2016`, :cite:`Spantini2017` .

**Contents**

.. toctree::
   :maxdepth: 2

   example-gumbel-1d.ipynb
   example-beta-1d.ipynb
   example-banana-2d.ipynb
   example-BOD-4d.ipynb
   example-sequential-stocvol-6d.ipynb
