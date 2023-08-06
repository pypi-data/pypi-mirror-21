Building Transport Maps
=======================

Before exploring the capabilities of the software we need to set some notation and definitions.

**Notation and definitions**

In the following we will denote by :math:`\nu_\pi` a probability distribution with density :math:`\pi:\mathbb{R}^d \rightarrow \mathbb{R}_+`, possibly unnormalized but integrable (i.e. :math:`\int \pi < \infty`).
A **transport map** is a map :math:`T:\mathbb{R}^d \rightarrow \mathbb{R}^d`.

We define the **pushforward** of :math:`\pi` under :math:`T` as the density

.. math::

   T_\sharp \pi({\bf x}) := \pi \circ T^{-1}({\bf x}) \; \left\vert \nabla T^{-1} \right\vert

We define the **pullback** of :math:`\pi` under :math:`T` as the density

.. math::

   T^\sharp \pi({\bf x}) := \pi \circ T({\bf x}) \; \left\vert \nabla T \right\vert

Under appropriate regularity assumptions on :math:`T`, these transformations define associated measures :math:`\nu_{T_\sharp \pi}` and :math:`\nu_{T^\sharp \pi}` :cite:`Villani2009`. We focus here exclusively on invertible transports (set :math:`\mathcal{T}`) and mainly (but not only) on Knothe-Rosenblatt rearrangements :cite:`Knothe1957`, :cite:`Rosenblatt1952`, i.e lower triangular ones:

.. math::

   T({\bf x}) = \left[
   \begin{array}{l}
   T_1(x_1) \\
   T_2(x_1, x_2) \\
   \;\;\;\vdots\\
   T_d(x_1,\ldots,x_d)
   \end{array}
   \right] \;.

We denote the set of Knothe-Rosenblatt rearrangements by :math:`\mathcal{T}_\triangle \subset \mathcal{T}`. Under relatively mild conditions (:math:`\nu_{\pi_1}` and :math:`\nu_{\pi_2}` absolutely continuous, which is satisfied if they have desities with respect to the Lebesgue measure) there exist :math:`T\in\mathcal{T}_\triangle` such that :math:`T_\sharp \pi_1 = \pi_2` (and :math:`T^\sharp \pi_2 = \pi_1`).

**Contents**

The following examples are designed to drive you through the capabilities of the software. We start with some simple ones and we build up on them when we move toward more complex problems. The user is thus suggested to go through each of the examples in an ordered way.

.. toctree::
   :maxdepth: 2

   examples-direct-transport.rst
   examples-transport-from-samples.rst
