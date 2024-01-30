# CMAKE 和 CPP 经验
## lib and dll

    lib 在编译时使用，dll在runtime时使用。
    windows下使用msvc生成dll比较麻烦，但是GNU会简单一些

## 关于头文件

### 重复引用/菱形引用
在文件首使用下列说明符就可以解决
``` cpp
#progma once
```
或者
``` cpp
#IFNOTDEFINE
#DEFINE
```
推荐前者
### 左值右值
有地址->左值 
不是左值+有地址无法操作，比如临时变量->右值

`i++` 右值，返回的是i的值
`++i` 左值，返回的是i本身

### 引用 指针 const mutable
都const了就别想怎么修改人家了，const函数内的成员都不可以被修改，除非那个变量是mutable（用处少）

普通引用无法引用const变量，但是给这个引用也加一个const就可以了

右值引用可以引用右值/临时变量

`return *this;` 是在非静态成员函数中使用返回对象本身或者克隆

指针也是一个变量，里面储存的是内存地址，而不是对象本身，就是一段内存地址。
所以指针指向的都是地址，而不是对象本身，所以指针指向的对象可以改变。也就是为什么指针赋值是会有变量的取地址。`int *p = &a;` 这里的`&`是取地址符，而不是引用符。

T * variable; 代表这个变量是一个指针，指向T类型的变量，*在这是说明符，而不是解引用.
### 万能引用
只有模板和auto关键字两种情况是万能引用
```cpp
template<typaname T>
T func1(T &&p1){return};

int a =10;
auto && i =a;
```
万能引用的效果是，如果传入的是左值，那么T就是左值引用，如果传入的是右值，那么T就是右值引用，再配合forward就可以完美转发。

左值引用在特定情况下也可以绑定右值，加上const就可以了
```cpp
const int & i = 10;
```

### 完美转发
使用```std::forward<T>(para)```来完美转发，这样就可以保证传进来的参数是什么类型，就以什么类型传出去，而不是被转换成左值或者右值。作用和意义是减少拷贝构造，提高效率。


```cpp
template<typename T>
CData* Creator(T&& t) {
    return new CData(std::forward<T>(t));
    //return new CData(t); // 会调用拷贝构造函数, 无法区分左值和右值
}
int main(void) {
    std::string str1 = "hello";
    std::string str2 = " world";
    CData* p1 = Creator(str1);        // 参数折叠为左值引用，调用CData构造函数
    CData* p2 = Creator(str1 + str2); // 参数折叠为右值引用，通过std::forward转发给CData，调用移动构造函数
    delete p2;
    delete p1;

    return 0;
}
```



### 引用折叠
所有右值引用折叠到右值引用上仍然是一个右值引用。（A&& && 变成 A&&）。
所有的其他引用类型之间的折叠都将变成左值引用。 （A& & 变成 A&; A& && 变成 A&; A&& & 变成 A&）。参数被一个左值或左值引用初始化，那么引用将折叠为左值引用。（即：T&& & –> T&）

简单来说：右值经过T&&参数传递，类型保持不变还是右值（引用）；而左值经过T&&变为普通的左值引用。
```cpp
template<typename T>
void func(T&& arg);

int main() {
  int a = 5;
  func(a);  // arg为int&，引用折叠为左值引用

  func(10);  // arg为int&&，引用折叠为右值引用

  int& ref = a;
  func(ref);  // arg为int&，引用不能折叠
}
```



### lambda
基本结构 `[]{}` 或者完全体 `[]()->return{}(parameter)`
``` cpp
int i =1;
auto c  = [i](int test_para){
    std::out<<i<<","<<test_para;
    return para;
}(23)
// output: 1 23

```
常用场景： 当他作为函数指针`(e.g: void(*)(int))`的时候，作为参数传递，有点闭包的感觉 （注意捕获列表[]要为空）
如果要捕获变量可以使用STL里的`<functional>`，将形参类型指定为 `std:function<T(T)>`

### inline 内联函数
用空间换效率，编译后文件会变大
如果类函数在类hpp内实现，那么它默认就是inline的
### explicit 关键字
```cpp

class Foo {
public:
    explicit Foo(int i) {}
};

void bar(Foo foo) {}

int main() {
    bar(Foo(123)); // 编译通过
    bar(123); // 编译错误：无法将整数转换为 Foo 类型
    return 0;
}

```
explicit 关键字可以帮助我们防止意外的类型转换和构造函数的错误使用，使程序更加安全和稳定。

### 友元
声明写在类内任何地方，这样声明的`friend`类/函数就可以访问这个类的private成员
破坏封装性，不如提供个接口来访问

可以用友元重载运算符，让自己写的类兼容某些运算，比如输出输出流, 这样可以链式编程。说到重载运算符，他就应该返回ostream的引用，要返回个对象这样才能继续链式调用运算符

### 重载运算符
关键字是operator
对`()`的重载是functor
`>>`重载时记得返回引用
`=`重载返回*this
移动和复制构造和等号运算符重载一起出现，注意如果类内有const成员变量，那么编译器不会自动生成移动构造。

### 继承和多态
父类指针可以指向子类---引申出多态的重要用法
当父类指针指向的是子类，并且调用了函数，这个函数还是个虚函数，那么就会执行子类的虚函数，否则的话执行父类的函数。**从中也可以提炼出一句话：CPP指针指向的对象可能和指针的类型不完全一直（父指子）**
当父指子的时候，使用typeid检测指针指向的对象的类名，会返回这个对象的真正类名，即子类类名(仅限虚函数)。


纯虚类不可以生成对象，从而避免出错。
### 浅拷贝
```cpp
class A{
    public:
        int* a;
};

A a1;
A b1=a1;//a1.a和b1.a指向的是同一个内存地址
```

两个指针指向同一个地方，这样在析构的时候同一个地方被析构两次，必出错。
解决办法：复制构造函数，复制时给对象开辟一块新内存，然后把东西移动过去

### 智能指针
用了智能指针就不要再手动delete了！
能使用智能指针就使用，除了：

·网络传输函数
·C语言的文件操作
·数组


初始化`shared_ptr`推荐用`make_shared<T>()`
初始化`unique_ptr`推荐用`make_unique<T>()`

两个智能指针交换有`swap`函数

`weak_ptr`可以解决循环引用，配合`shared_ptr`一起使用，循环引用的意思是堆上内存互相指向，无法被释放。

`unique_ptr` 即不可以两个指针共享同一个内存/指向同一个地方，也就是不可以复制构造，即
```cpp
p2 =p1;//不可以
p2(p1);//不可以

//因为这样两个指针指向同一个内存就不是unique了
```
自然而然，move构造当然可以，因为被move了
```cpp
p2 =std::move(p1);//不可以
p2(std::move(p1));//不可以

//因为把内存移动了，原有的指针不再指向那个内存
```
这样同时也解决了循环引用问题，因为根本不存在这种情况

`unique_ptr`可以通过move转换成shared_ptr但这是单向的

用哪种智能指针主要是考虑这个对象会不会有共用内存的情况。
### 模板
类外写成员函数，记得加上typename，typename 的意义是告诉后面的是个类型，一般是在类内有个using关键字的情况下要注意。

### STL

#### 容器

list是不可以index取值的，也就是没有重载`[]` 运算符

如果是频繁修改查找 --- 无序容器
如果是频繁增加删除 --- 有序容器
### 多线程
#### 基本概念
子线程创建后理应进行`detach()` 或者`join()` 操作保证主进程结束后资源不会被意外销毁
`detach()`的原理是，会让Cpp运行库接管资源，所以在主线程结束后也不会出现资源被销毁的问题，但是值得注意的是，给这样的子线程传参时，不能用指针传递参数，因为在线程间传递时，指针传递的是同一个内存地址，有可能导致资源意外销毁！

隐式转换是发生在子线程里的，所以尽量避免。

传参：值类型传值，类类型传引用，如果想在子进程里修改传参的值，使用`std::ref` 
```cpp
MyThread(func,std::ref(varible))
``` 
#### 进程锁
用`std::lock_guard<std::mutex>` 来保证不会忘记解锁，同时注意作用范围，`lock_guard`和单纯`mutex`的关系类似于指针和智能指针。

死锁问题用 `std::lock`+`std::adopt_lock` 解决，前者规定所得顺序，后者只赋予`lock_guard`开锁功能


## CMAKE 语法进阶
### 项目组织
当某个库（lib）添加了某个include路径，使用这个库的项目就不用再次声明要包含这个路径 （需要PUBLIC 下同）
``` cmake
target_include_dictionaries(libname PUBLIC/PRIVATE PATH)
```
同理，链接库也是这样，某个库链接过某个库，则不用重复链接
``` cmake
target_link_libraries(libname PUBLIC/PRIVATE PATH)
```
推荐这么做，避免CMAKE臃肿

另外应尽量避免使用对应的全局命令，如：`link_libraries` `include_dictionaries` 
