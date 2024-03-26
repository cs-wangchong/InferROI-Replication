from app.intention import Intention

SYSTEM_PROMPT = "You are an expert in identifying resource leaks in Java programs."

PROMPT_TEMPLATE  = '''Analyze the information about resource leaks in the provided code snippet below. First, resolve the types of the involved objects. Then, identify the types representing leakable resources. Next, identify the API/method calls for acquiring the resources. After that, identify the API/method calls for releasing the acquired resources. Finally, identify the if-conditions for checking whether the acquired resources are closed or unclosed.

Desired format:
Leakable Resources: 
<resource type>: <resource variable>

API/method Calls for Acquiring Resources:
line <line number>: `<API call>` %ss `<resource variable>` resource

API/method Calls for Releasing Resources: 
line <line number>: `<API call>` %ss `<resource variable>` resource

If-conditions for Checking Resources closed or not:
line <line number> `<if-condition>` %ss `<resource variable>` resource

Code Snippet: ```java
{code}
```
''' % (Intention.OPEN, Intention.CLOSE, Intention.VALIDATE)



# PROMPT_TEMPLATE = '''Analyze the information about resource leaks in the provided code snippet below. First resolve the types of the involved objects, then identify the types representing leakable resources, then identify the API/method calls for acquiring the resources, then identify the API/method calls for releasing the acquired resources, and finally identify the if-contidtions for checking whether the acquired resources are closed/unclosed.

# Desired format:
# Leakable Resources: 
# <resource type>: <resource variable>

# API/method Calls for Acquiring Resources:
# line <line number>: `<API call>` %ss `<resource variable>` resource

# API/method Calls for Releasing Resources: 
# line <line number>: `<API call>` %ss `<resource variable>` resource

# If-conditions for Checking Resources:
# line <line number> `<if-condition>` %ss `<resource variable>` resource

# Code Snippet: """java
# {code}
# """
# '''  % (Intention.OPEN, Intention.CLOSE, Intention.VALIDATE)