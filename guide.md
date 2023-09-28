## To reate virtual environment
  ```python  
    python -m venv env_name
  ```

## To install requirements 
   ```python 
    pip install requirements.txt 
    # this file presents inside jobportal directory. 
   ```


## ⚠️ Important
<b> To create requirements.txt</b>
 ```python 
     pip freeze >requirements.txt 
     # (run this command whenever you install new module. Dont forget this)

```

 ## Activating the Virtual Environment

If you're currently located within the `Jobportal` directory, execute the following command in your command line interface (CMD / Powershell):

```sh
# Navigate to the Jobportal directory
cd path\to\Jobportal

# Activate the virtual environment
..\env\Scripts\activate
```

If you're inside a directory where `jobportal` and `env` directories located, you can run following command:
  
```sh

# Activate the virtual environment
   env\Scripts\activate

   #You can use tab key to use auto completion.
```
