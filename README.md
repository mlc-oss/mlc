# MLC: Machine Learning on Container
![GitHub Actions CI](https://github.com/rapsealk/mlc/workflows/Lint/badge.svg)
![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg?logo=python)
![Docker](https://img.shields.io/badge/Docker-Runtime-blue.svg?logo=docker)

```bash
>> python -m pip install -e .
```
```python
import mlc
```
[도메인 초안]
![image](https://user-images.githubusercontent.com/26168539/143554134-9831732d-4641-4f47-aadb-613626e13d90.png)


[기술 스택]
![image](https://user-images.githubusercontent.com/26168539/143553884-870b81eb-0c58-414d-9708-fec507272f79.png)
 

[기본 MLC 기능]  

1. 제공되는 데이터 플랫폼은 주기적으로 (실시간일경우 난이도 급상) 데이터를 수집하고 분석  
2. 요청을 통해 데이터 플랫폼의 구성과 규모 선택  
3.데이터를 처리할 worker는 분석 규모에 따라 스케일링되야함 (k8s 기능으로 가능)  
4.workflow를 통해 종속성 있는 데이터를 분석 가능해야함  
5.장애, 중단된 작업을 관리하거나 자동화 할수 있어야함  


[특화 사항]
1.Kubelet을 통해 K8S 클러스터를 하이브리드로 제공
2.LB , MQ등 컴포넌트 구성을 각 CSP의 상품으로 선택 
