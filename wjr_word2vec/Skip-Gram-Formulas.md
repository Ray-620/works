## Skip-Gram模型推导

推理过程如下：

假设我们有一个长度为V的字库（$\theta$），那么目标函数是：
$$
\mathop{argmax}_\theta\prod_{w\in Text}\prod _{c\in C(w) }P(c|w;\theta)
$$
​                                                                       $\omega$是中心词，c是上下文词

然后我们可以取对数：
$$
\mathop{argmax}_\theta\sum_{(w,c)\in D}\log p(c|w;\theta)
$$
P(c|w)等价于:
$$
\mathop{argmax}_\theta\sum_{(w,c)\in D}\log {e^{u_c.v_m}\over\sum_{c'\in U}e^{u_{c'}.v_m}}
$$
化简得 :
$$
\mathop{argmax}_{u,v}\sum_{(w,c)\in D}(u_c.v_m-\log (\sum_{c'\in U }e^{u_{c'}.v_w}))
$$


