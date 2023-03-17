## 编写进动模型的红噪声函数和调用函数
import numpy as np
from enterprise.signals import (deterministic_signals, parameter, signal_base,
                                utils)

@signal_base.function
def RedNoise_delay(toas, t0, P, a1, a2, k):

    """
    ##定义红噪声函数

    :param a1: 
        第一次谐波的振幅(s)
    :param a2:
        第二次谐波的振幅(s)
    :param P:
        进动周期(s)
    :param Wp:
        进动频率
    :param k:
        任意偏移(s)
    :param t:
        pulsar toas in seconds(s)
    :param t0:
        选取的一个0时刻(s)
    # :param K: 
    #     与J1939的自旋向下扭矩的强度成正比
    # :param O: 
    #     角动量和对称轴的夹角
    # :param X:
    #     偶极矩和对称轴的夹角

    """

    #define Wp
    Wp = 2*np.pi/P  

    # # define a1 and a2
    # a1 = K*O*np.sin(2*X)/(1+O**2)
    # a2 = K*O**2*np.sin(X)**2/(4*(1+O**2))

    # residuals
    res = k + a1*np.sin(Wp*(toas-t0)) - a2*np.sin(2*Wp*(toas-t0))

    return res


def RedNoise_delay_block(t0_lower=4600000000, t0_upper=6300000000,
                         P_lower=432000000, P_upper=4320000000,
                         a1_lower=0.000001, a1_upper=0.001,
                         a2_lower=0.000001, a2_upper=0.001,
                         k_lower=-0.001, k_upper=0.001,
                         name='RedNoise',):

    """
    调用RedNoise_delay函数
    
    """

    # RedNoise_delay parameters
    # t_name = '{}_log10_t'.format(name)
    # log10_t_RedNoise = parameter.Uniform(t_lower, t_upper)(t_name)

    # Tmin = tmin[0]
    # Tmax = tmax[0]
    t0_name = '{}_t0'.format(name)
    t0_RedNoise = parameter.Uniform(t0_lower, t0_upper)(t0_name)

    P_name = '{}_P'.format(name)
    P_RedNoise = parameter.Uniform(P_lower, P_upper)(P_name)

    a1_name = '{}_a1'.format(name)
    a1_RedNoise = parameter.Uniform(a1_lower, a1_upper)(a1_name)

    a2_name = '{}_a2'.format(name)
    a2_RedNoise = parameter.Uniform(a2_lower, a2_upper)(a2_name)

    k_name = '{}_k'.format(name)
    k_RedNoise = parameter.Uniform(k_lower, k_upper)(k_name)


    # 红噪声残差
    RedNoise_d = RedNoise_delay(t0=t0_RedNoise, 
                                P=P_RedNoise, a1=a1_RedNoise, 
                                a2=a2_RedNoise, k=k_RedNoise)
    
    RedNoise = deterministic_signals.Deterministic(RedNoise_d, name=name)

    return RedNoise
