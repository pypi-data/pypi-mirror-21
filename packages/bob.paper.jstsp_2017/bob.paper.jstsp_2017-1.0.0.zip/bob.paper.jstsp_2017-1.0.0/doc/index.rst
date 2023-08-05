.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Mon 3 Apr 13:43:22 2017

======================================================================
 Package for paper published in J-STSP 2017 on PAD fusion and ASV-PAD 
======================================================================


If you use this package, please cite the following paper::

    @article{KorshunovJSTSP2017,
        author = {P. Korshunov and S. Marcel},
        title = {Impact of score fusion on voice biometrics and presentation attack detection in cross-database evaluations},
        year = {2017},
        journal = {IEEE Journal of Selected Topics in Signal Processing},
    }

This package contains scripts to reproduce the results from the paper. The package also provides score files for i-vector based automatic speaker verification (ASV) system and PAD systems that are used to produce the error rates and plots presented in the paper.


Reproducing results of the paper
--------------------------------

Scores of ASV and PAD systems can be found in folder `scores`. 

To create a joint ASV-PAD system, the scores can be fused using Logistic Regression classifier (as per the paper), resulting in another set of scores, by running the following:

.. code-block:: sh

    $ ./fuse_asv_pad_scores.py -e scores/asv_scores -p scores/pad_scores - o fused_system

The script will generate fused scores inside the folder `fused_system`. 

To plot histograms distribution for ASV system in `licit` scenario, as presented in Figure 4a of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_asv_results.py -d scores/asv_scores/scores-dev-real -e scores/asv_scores/scores-eval-real 
        -t scores/asv_scores/scores-dev-attack -f scores/asv_scores/scores-eval-attack --scenario licit

To plot histograms distribution for ASV system in `spoof` scenario, as presented in Figure 4b of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_asv_results.py -d scores/asv_scores/scores-dev-real -e scores/asv_scores/scores-eval-real 
	-t scores/asv_scores/scores-dev-attack -f scores/asv_scores/scores-eval-attack --scenario spoof 

To plot histograms distribution for PAD system , as presented in Figure 4c of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_pad_results.py -d scores/pad_system/scores-dev-real -e scores/pad_system/scores-eval-real 
	-t scores/pad_system/scores-dev-attack -f scores/pad_system/scores-eval-attack

The script creates PDF files for DET curves, histogram distributions for dev and eval sets, and writes main statistics such as FAR, FRR, and EER into a text file.



To plot a scatter plot presented in Figure 5a of the paper, run the following:

.. code-block:: sh

    $ bin/plot_scatter.py -e scores/asv_scores -p scores/pad_scores 

The script will generate PDF scatter plots inside `fused_score` folder for Train, Dev, and Test sets.

To plot Figure 5b and Figure 5c, please run the following

To plot a scatter plot presented in Figure 5a of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_on_demand.py scores/fused_system/scores-dev-fused-real scores/fused_system/scores-eval-fused-real 
	scores/fused_system/scores-dev-fused-attack scores/fused_system/scores-eval-fused-attack -i 7 -c eer


Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _BEAT: https://www.beat-eu.org/platform/
.. _AVspoof: https://www.idiap.ch/dataset/avspoof

