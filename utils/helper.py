import os, sys
from os.path import dirname as up
import time
from typing import Generator
import re
import logging

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils.common_libraries import *
from utils.constants import *

def get_realtime_response(user_prompt: str, **kwargs) -> Generator[str, None, None]:
    """
    This function takes a user prompt as a string and returns a realtime response using a simple keyword-based mechanism.
    """
    try:
        # Convert prompt to lowercase for case-insensitive matching
        prompt_lower = user_prompt.lower()
        
        # Define responses for different keywords
        responses = {
            "hello": "Hello! I'm CodeOn, your AI coding assistant. How can I help you today?",
            "help": "I can help you with:\n1. Writing and optimizing code\n2. Debugging and problem-solving\n3. Explaining programming concepts\n4. Implementing algorithms\n5. Code review and best practices\n\nJust ask me anything!",
            "python": "Here's a simple Python example:\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('World'))\n```",
            "javascript": "Here's a simple JavaScript example:\n```javascript\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n\nconsole.log(greet('World'));\n```",
            "debug": "To debug your code:\n1. Add print statements or use a debugger\n2. Check for syntax errors\n3. Verify input/output\n4. Test edge cases\n5. Review error messages",
            "fibonacci": """Here's a Python implementation of the Fibonacci sequence with multiple approaches:

1. Recursive approach:
```python
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
```

2. Iterative approach (more efficient):
```python
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

3. Generator approach (for sequence):
```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usage example:
# fib = fibonacci_generator()
# for _ in range(10):
#     print(next(fib))
```

The iterative approach is recommended for better performance, especially for larger numbers.""",
            "gradient": """Here's a Python implementation of Gradient Descent:

```python
import numpy as np

def gradient_descent(x, y, learning_rate=0.01, num_iterations=1000):
    # Initialize parameters
    m = len(x)
    theta = np.zeros(2)  # [intercept, slope]
    
    # Gradient descent
    for _ in range(num_iterations):
        # Predictions
        y_pred = theta[0] + theta[1] * x
        
        # Compute gradients
        gradient_0 = (-2/m) * np.sum(y - y_pred)
        gradient_1 = (-2/m) * np.sum((y - y_pred) * x)
        
        # Update parameters
        theta[0] = theta[0] - learning_rate * gradient_0
        theta[1] = theta[1] - learning_rate * gradient_1
    
    return theta

# Example usage:
# x = np.array([1, 2, 3, 4, 5])
# y = np.array([2, 4, 5, 4, 5])
# theta = gradient_descent(x, y)
# print(f"Intercept: {theta[0]:.2f}, Slope: {theta[1]:.2f}")
```

This implementation:
1. Uses linear regression as an example
2. Implements batch gradient descent
3. Updates parameters using the gradient of the loss function
4. Includes learning rate and number of iterations as parameters""",
            "ai system": """Here's a high-level overview of building an AI coding system like ChatGPT:

1. Core Components:
```python
# 1. Model Architecture
class CodeAIModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
        self.model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
    
    def generate_code(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=1000)
        return self.tokenizer.decode(outputs[0])

# 2. Training Pipeline
class TrainingPipeline:
    def __init__(self):
        self.dataset = load_code_dataset()  # Load from GitHub, Stack Overflow, etc.
        self.model = CodeAIModel()
    
    def train(self):
        # Fine-tune on code-specific tasks
        pass

# 3. API Interface
from fastapi import FastAPI
app = FastAPI()

@app.post("/generate")
async def generate_code(prompt: str):
    model = CodeAIModel()
    return {"code": model.generate_code(prompt)}
```

2. Key Features to Implement:
- Code understanding and generation
- Context awareness
- Error handling and debugging
- Code optimization
- Documentation generation
- Multiple language support

3. Required Technologies:
- Large Language Models (LLMs)
- Vector databases for code search
- Code analysis tools
- API frameworks
- Cloud infrastructure

4. Development Steps:
1. Start with a pre-trained model (CodeLlama, GPT, etc.)
2. Fine-tune on code-specific datasets
3. Implement code analysis and generation
4. Add context management
5. Build API and interface
6. Deploy and scale

5. Best Practices:
- Use version control
- Implement proper error handling
- Add logging and monitoring
- Ensure security measures
- Regular model updates
- User feedback loop

Remember: Building a full system like ChatGPT requires significant resources and expertise in ML, software engineering, and infrastructure.""",
            "sort": """Here are different sorting algorithms implemented in Python:

1. Bubble Sort:
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

2. Quick Sort:
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

3. Merge Sort:
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

Time Complexities:
- Bubble Sort: O(n²)
- Quick Sort: O(n log n) average case, O(n²) worst case
- Merge Sort: O(n log n)

Space Complexities:
- Bubble Sort: O(1)
- Quick Sort: O(log n)
- Merge Sort: O(n)""",
            "tree": """Here's an implementation of a Binary Search Tree in Python:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# Usage example:
# bst = BinarySearchTree()
# bst.insert(5)
# bst.insert(3)
# bst.insert(7)
# print(bst.inorder_traversal())  # [3, 5, 7]
```

Key operations:
1. Insert: O(log n) average case, O(n) worst case
2. Search: O(log n) average case, O(n) worst case
3. Inorder Traversal: O(n)

The tree maintains the property that for any node:
- All values in the left subtree are less than the node's value
- All values in the right subtree are greater than the node's value""",
            "graph": """Here's an implementation of a Graph in Python using adjacency lists:

```python
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
    
    def bfs(self, start):
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            vertex = queue.pop(0)
            print(vertex, end=' ')
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    
    def dfs(self, start):
        visited = set()
        self._dfs_recursive(start, visited)
    
    def _dfs_recursive(self, vertex, visited):
        visited.add(vertex)
        print(vertex, end=' ')
        
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited)
    
    def has_cycle(self):
        visited = set()
        rec_stack = set()
        
        def dfs_cycle(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(vertex)
            return False
        
        for vertex in self.graph:
            if vertex not in visited:
                if dfs_cycle(vertex):
                    return True
        return False

# Usage example:
# g = Graph()
# g.add_edge(0, 1)
# g.add_edge(0, 2)
# g.add_edge(1, 2)
# g.add_edge(2, 0)
# g.add_edge(2, 3)
# g.add_edge(3, 3)
# print("BFS starting from vertex 2:")
# g.bfs(2)
# print("\nDFS starting from vertex 2:")
# g.dfs(2)
# print("\nHas cycle:", g.has_cycle())
```

Key features:
1. Adjacency list representation
2. BFS traversal
3. DFS traversal
4. Cycle detection
5. Directed graph support

Time Complexities:
- Add Edge: O(1)
- BFS/DFS: O(V + E) where V is vertices and E is edges
- Cycle Detection: O(V + E)""",
            "dp": """Here are some common Dynamic Programming problems in Python:

1. Fibonacci with Memoization:
```python
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]
```

2. Longest Common Subsequence:
```python
def lcs(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

3. 0/1 Knapsack:
```python
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]
```

Key concepts:
1. Memoization (top-down)
2. Tabulation (bottom-up)
3. State transitions
4. Optimal substructure
5. Overlapping subproblems

Time Complexities:
- Fibonacci: O(n) with memoization
- LCS: O(mn)
- Knapsack: O(nW)
- Matrix Chain: O(n³)""",
            "regex": """Here's a comprehensive guide to Regular Expressions in Python:

```python
import re

# Basic Patterns
text = "Hello, World! 123"

# Match digits
digits = re.findall(r'\d+', text)  # ['123']

# Match words
words = re.findall(r'\w+', text)  # ['Hello', 'World', '123']

# Match specific characters
special = re.findall(r'[!,.]+', text)  # [',', '!']

# Common Patterns
patterns = {
    'email': r'[\w\.-]+@[\w\.-]+\.\w+',
    'phone': r'\d{3}[-.]?\d{3}[-.]?\d{4}',
    'url': r'https?://(?:[\w-]+\.)+[\w-]+(?:/[\w-./?%&=]*)?',
    'date': r'\d{4}-\d{2}-\d{2}',
    'ip': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
}

# Example usage
def validate_pattern(text, pattern):
    return bool(re.match(pattern, text))

# Common regex functions
def regex_examples():
    text = "Contact us at support@example.com or call 123-456-7890"
    
    # Search
    match = re.search(r'\d{3}-\d{3}-\d{4}', text)
    if match:
        print(f"Found phone: {match.group()}")
    
    # Find all
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    print(f"Found emails: {emails}")
    
    # Replace
    masked = re.sub(r'\d{3}-\d{3}-\d{4}', 'XXX-XXX-XXXX', text)
    print(f"Masked text: {masked}")
    
    # Split
    words = re.split(r'\W+', text)
    print(f"Split words: {words}")
```

Key concepts:
1. Character classes
2. Quantifiers
3. Groups and capturing
4. Lookahead/lookbehind
5. Flags and modifiers""",
            "async": """Here's a guide to Asynchronous Programming in Python:

```python
import asyncio
import aiohttp
import time

# Basic async function
async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Async with multiple tasks
async def main():
    tasks = [
        asyncio.create_task(hello()),
        asyncio.create_task(hello()),
        asyncio.create_task(hello())
    ]
    await asyncio.gather(*tasks)

# Async HTTP requests
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_multiple_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Async context manager
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(1)

# Async generator
async def async_range(stop):
    for i in range(stop):
        yield i
        await asyncio.sleep(0.1)

# Usage examples
async def examples():
    # Basic async
    await hello()
    
    # Multiple tasks
    await main()
    
    # HTTP requests
    urls = [
        "https://api.github.com/users/python",
        "https://api.github.com/users/django",
        "https://api.github.com/users/flask"
    ]
    results = await fetch_multiple_urls(urls)
    
    # Async context manager
    async with AsyncResource() as resource:
        print("Using resource")
        await asyncio.sleep(1)
    
    # Async generator
    async for i in async_range(5):
        print(i)

# Run the examples
if __name__ == "__main__":
    asyncio.run(examples())
```

Key concepts:
1. Coroutines
2. Event loop
3. Tasks
4. Async context managers
5. Async generators

Best practices:
1. Use `asyncio.gather()` for concurrent tasks
2. Proper resource management
3. Error handling
4. Timeout management
5. Cancellation handling

Common use cases:
1. Web scraping
2. API calls
3. Database operations
4. File I/O
5. Network programming""",
            "test": """Here's a comprehensive guide to Testing in Python:

```python
import unittest
import pytest
from unittest.mock import Mock, patch

# Unit Testing with unittest
class Calculator:
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(0, 0), 0)

# Testing with pytest
def test_calculator_add():
    calc = Calculator()
    assert calc.add(3, 5) == 8
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0

# Mocking
class Database:
    def get_user(self, user_id):
        # Simulate database call
        pass

class UserService:
    def __init__(self, db):
        self.db = db
    
    def get_user_name(self, user_id):
        user = self.db.get_user(user_id)
        return user.name if user else None

def test_user_service():
    # Create mock database
    mock_db = Mock()
    mock_db.get_user.return_value = Mock(name="John")
    
    # Create service with mock
    service = UserService(mock_db)
    
    # Test
    assert service.get_user_name(1) == "John"
    mock_db.get_user.assert_called_once_with(1)

# Fixtures
@pytest.fixture
def calculator():
    return Calculator()

def test_calculator_with_fixture(calculator):
    assert calculator.add(3, 5) == 8
    assert calculator.subtract(5, 3) == 2

# Parameterized tests
@pytest.mark.parametrize("x,y,expected", [
    (3, 5, 8),
    (-1, 1, 0),
    (0, 0, 0)
])
def test_add_parameterized(calculator, x, y, expected):
    assert calculator.add(x, y) == expected

# Async testing
import asyncio

async def async_function():
    await asyncio.sleep(0.1)
    return "result"

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == "result"

# Test coverage
def test_with_coverage():
    calc = Calculator()
    assert calc.add(3, 5) == 8
    assert calc.subtract(5, 3) == 2
```

Key concepts:
1. Unit testing
2. Test fixtures
3. Mocking
4. Parameterized tests
5. Async testing

Best practices:
1. Test isolation
2. Meaningful assertions
3. Test coverage
4. Test organization
5. Error handling

Common testing patterns:
1. Arrange-Act-Assert
2. Given-When-Then
3. Test doubles
4. Test suites
5. Test runners""",
            "design": """Here are some common Design Patterns in Python:

1. Singleton Pattern:
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

2. Factory Pattern:
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError("Unknown animal type")
```

3. Observer Pattern:
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def update(self, message):
        print(f"Received message: {message}")
```

4. Decorator Pattern:
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b
```

Key concepts:
1. Creational patterns
2. Structural patterns
3. Behavioral patterns
4. SOLID principles
5. Code reusability""",
            "web": """Here's a guide to Web Development with Python:

1. Flask Basic Setup:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.get_json()
        # Process data
        return jsonify({"status": "success"})
    return jsonify({"data": "sample data"})

if __name__ == '__main__':
    app.run(debug=True)
```

2. FastAPI Example:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

3. Database Integration:
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

# Database setup
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

4. RESTful API Best Practices:
- Use proper HTTP methods
- Implement authentication
- Handle errors gracefully
- Version your APIs
- Document with OpenAPI/Swagger

5. Frontend Integration:
```python
# Serve static files
from flask import send_from_directory

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# API endpoints for frontend
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)
```

Key concepts:
1. HTTP methods
2. REST principles
3. Database integration
4. Authentication
5. API documentation""",
            "data": """Here's a guide to Data Structures in Python:

1. Linked List:
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def display(self):
        current = self.head
        while current:
            print(current.data, end=' -> ')
            current = current.next
        print('None')
```

2. Stack:
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Stack is empty")
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Stack is empty")
    
    def is_empty(self):
        return len(self.items) == 0
```

3. Queue:
```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        raise IndexError("Queue is empty")
    
    def is_empty(self):
        return len(self.items) == 0
```

4. Hash Table:
```python
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[index].append([key, value])
    
    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        raise KeyError(key)
```

Time Complexities:
- Linked List: O(n) for search, O(1) for insert/delete at head
- Stack: O(1) for push/pop
- Queue: O(1) for enqueue/dequeue
- Hash Table: O(1) average case for insert/search

Space Complexities:
- Linked List: O(n)
- Stack: O(n)
- Queue: O(n)
- Hash Table: O(n)""",
            "security": """Here's a guide to Security Best Practices in Python:

1. Password Hashing:
```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

2. Input Validation:
```python
from typing import Optional
import re

def validate_email(email: str) -> Optional[str]:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email

def sanitize_input(user_input: str) -> str:
    # Remove potentially dangerous characters
    return re.sub(r'[<>]', '', user_input)
```

3. Secure File Operations:
```python
import os
from pathlib import Path

def secure_file_operations():
    # Use pathlib for safe path handling
    file_path = Path("data") / "user_files" / "document.txt"
    
    # Check file permissions
    if not os.access(file_path, os.R_OK):
        raise PermissionError("No read permission")
    
    # Safe file reading
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Safe file writing
    with open(file_path, 'w') as f:
        f.write(content)
```

4. API Security:
```python
from functools import wraps
from flask import request, abort
import jwt

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401)
        try:
            # Verify JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return f(*args, **kwargs)
        except jwt.InvalidTokenError:
            abort(401)
    return decorated
```

5. Database Security:
```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def secure_db_connection():
    conn = sqlite3.connect('database.db')
    try:
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    finally:
        conn.close()

def safe_query(query, params=None):
    with secure_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
```

Key Security Principles:
1. Never store plain text passwords
2. Validate and sanitize all input
3. Use parameterized queries
4. Implement proper authentication
5. Follow the principle of least privilege

Common Vulnerabilities to Avoid:
1. SQL Injection
2. XSS (Cross-Site Scripting)
3. CSRF (Cross-Site Request Forgery)
4. Insecure Deserialization
5. Broken Authentication"""
        }
        
        # Find matching response or use default
        response = None
        for keyword, resp in responses.items():
            if keyword in prompt_lower:
                response = resp
                break
        
        if not response:
            response = "I'm here to help with your coding tasks. You can ask me about:\n- Writing code\n- Debugging\n- Best practices\n- Algorithms\n- Or any other programming topic!"
        
        # Stream the response character by character
        for char in response:
            yield char
            time.sleep(0.01)  # Small delay for streaming effect
            
    except Exception as e:
        logger.error(f"Error in get_realtime_response: {str(e)}")
        yield f"I apologize, but I encountered an error: {str(e)}. Please check the console for more details."

def configure_generation():
    """
    Configure generation parameters
    """
    generation_config = {
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    
    return generation_config