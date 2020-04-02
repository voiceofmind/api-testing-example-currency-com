### To run tests (demo):
`cd` to the project directory<br/>
`python -m pytest -m unauthorized`
<br/>
<br/>
Required pytest (`pip3 install pytest`) or use venv from the project (`source project_directory/venv/bin/activate`)    
<br/>
#### Options:
Default environment is prod. Can be changed to test in test_config.py
<br/>

Run only those tests where authorization is not required:<br/>
`python -m pytest -m unauthorized`

Run all tests:
`python -m pytest`