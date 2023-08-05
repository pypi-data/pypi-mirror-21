
`mdconvert` uses a notebook's metadata to configure `nbconvert` actions.

# Usage

(Edit > Edit Notebook Metadata) and add a `nbconvert` key a notebook's `metadata`; the `value` is a list of lists - the `export_format` & an object with [`configurables`](http://nbconvert.readthedocs.io/en/latest/config_options.html), respectively.

> Edit the `metadata` with a cell magic.


```python
%reload_ext mdconvert
```


```python
%%metadata
nbconvert:
    - [markdown, {}]
```


    <IPython.core.display.Javascript object>



```python
!jupyter mdconvert README.ipynb
```

    [NbConvertApp] Converting notebook README.ipynb to html
    [MDConvertApp] Writing 1288 bytes to README.md
    [NbConvertApp] Conversions completed in 0.10619997978210449 seconds.


## `PostSaveContentsManager`

Have `mdconvert` create derived notebooks each time a notebook is saved.

        jupyter notebook --NotebookApp.contents_manager_class=mdconvert.PostSaveContentsManager
        
__or__ _install `mdconvert` as an extension_
        
        jupyter serverextension enable --py mdconvert

## Executing notebooks


```python
# !jupyter mdconvert README.ipynb --execute
```

    [MDConvertApp] Executing notebook with kernel: root
    [NbConvertApp] Converting notebook README.ipynb to html
    [MDConvertApp] Writing 1257 bytes to README.md
    [NbConvertApp] Conversions completed in 3.65071702003479 seconds.


## Executing with a different kernel


```python
# !jupyter mdconvert README.ipynb --execute --ExecutePreprocessor.kernel_name=py36
```

    [MDConvertApp] Executing notebook with kernel: py36
    [NbConvertApp] Converting notebook README.ipynb to html
    [MDConvertApp] Writing 1530 bytes to README.md
    [NbConvertApp] Conversions completed in 3.655313014984131 seconds.



```python
import mdconvert
mdconvert.__version__
```




    '0.1.0'


