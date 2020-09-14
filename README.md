# [MIT 6.034](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/)

Working through course materials for [MIT 6.034](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/).

### Materials

* [Course YouTube playlist](https://www.youtube.com/playlist?list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi)
    * Playlist order doesn't perfectly follow course flow (watch a lecture then scroll to bottom to see "Mega" video with related topic)
* Course materials:
    * [Online](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/index.htm)
    * [In this repo](6-034-fall-2010)
* [Text book](https://courses.csail.mit.edu/6.034f/ai3/rest.pdf) (hosted by MIT.edu so it feels legit)

### Working exercises
* Create a folder of each lab
    * Labs can be found as zip files in [`6-034-fall-2010/contents/assignments`](6-034-fall-2010/contents/assignments)
* Make a copy of the original lab file (i.e. copy `lab0.py` to `lab0_og.py`) for posterity
* Fill out solutions as instructed in the associated pdf in [`6-034-fall-2010/contents/assignments`](6-034-fall-2010/contents/assignments)
* Run lab tests in unzipped lab dir
    * A modified tester was made in root of repo (`tester.py`)
        * `tester.py` usage:
            * `~/mit6034 $ tester.py -l lab_dir`
            * `~/mit6034 $ tester.py -l labs/lab0`

### Python Version 2 vs 3
The course materials were written with python < 3.  
`cvt2py3.py` is a script to convert files to python 3.  
Almost definitely a better tool to do this change. 
I did this custom script cause I was curious to find out the changes needed.
* `cvt2py3.py` usage: 
    * `~/mit6034 $ cvt2py3.py -i python2_file.py`
    * `~/mit6034 $ cvt2py3.py -i labs/lab0/tests.py`
