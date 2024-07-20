# 二十三种设计模式
三个原则：1，单一原则：一个类只做一件事情。2，开闭原则：对扩展开放，对修改关闭。3，依赖倒置原则：依赖抽象而不依赖具体。
## 单例模式
- 特点：保证一个类仅有一个实例，并提供一个访问它的全局访问点。
- 实现方式：懒汉式（类创建时并没有给静态变量指定内存和创建实例，需要时再创建）、饿汉式、双重检查锁（检查是否为空指针，同时可以使用原子操作保证线程安全）、静态内部对象（>=C++11）。
- 应用场景举例：任务队列
- 关键: 构造函数私有化，这样无法从类外部创建，或者delete和default。静态成员变量指向唯一实例，提供静态方法返回唯一实例。记得静态成员变量要初始化。 懒汉模式要加锁，饿汉模式不用加锁。
```cpp
//懒汉模式 + 双重检查锁
class Singleton{
    private:
        Singleton(){}//构造函数私有化
        static Singleton* instance;
        static std::mutex m;
    public:
        static Singleton* getInstance(){
            if(instance==nullptr){
                std::lock_guard<std::mutex> lock(m);
                if(instance==nullptr){
                    instance=new Singleton();
                }
            }
        }
};
Singleton* Singleton::instance=nullptr;
```
利用新特性的静态内部对象,这样可以保证线程安全，因为静态成员变量只会初始化一次
```cpp
class Singleton{
    private:
        Singleton(){}//构造函数私有化
    public:
        static Singleton* getInstance(){
          static Singleton instance;
          return &instance; //注意函数返回的是指针，所以这里返回的是地址/引用
        }
};
```