# 英语基础概念
- [ ] 1. How to understand OOP?
  
    - Polymorphism  [pol-ee-MOR-fiz-um]
    - Inheritance [in-HER-i-tuhns]
    - Encapsulation [en-cap-suh-LAY-shuhn]
    - Abstraction
- [ ] 2. STACK vs HEAP
    - Stack: 
        - Don't have to manage memory
        - Limited size 
        - Lifetime of variables is limited to the scope of the block in which they are defined
    - Heap:
        - Have to manage memory
        - Large size
        - In cpp use new and delete to allocate and deallocate memory
- [ ] 3 explicit vs implicit
    - Explicit [ik-SPLIS-it]
    - Implicit [im-PLIS-it]
# Cpp14 new features
- [ ] Generic lambdas
- [ ] auto return type deduction

# Cpp 17 new features
- [ ] Structured Bindings - Decompose objects into their components like python
  
  ```cpp
    std::tuple<int, double, std::string> t = {1, 2.3, "example"};
    auto [x, y, z] = t;
  ```
- [ ] std::filesystem
    ```cpp
    #include <iostream>
    #include <filesystem>
    namespace fs = std::filesystem;

    int main() {
        fs::path p = "/example/directory";
        std::cout << "Is directory: " << fs::is_directory(p) << std::endl;
    }
    ```

  