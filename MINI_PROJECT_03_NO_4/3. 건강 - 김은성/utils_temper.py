import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 연도별 데이터 그래프 그리기 함수
def plot_yearly(data, title, y_label, color):
    plt.figure(figsize=(15, 7))
    
    # 데이터 플롯 (첫번째 열과 두번째 열 사용)
    plt.plot(data.iloc[:, 0], data.iloc[:, 1],'-o',
             color=color, label=y_label)
    
    # 그래프 설정
    plt.title(f"연도별 {title} 변화 (2010-2023)")
    plt.xlabel("연도")
    plt.ylabel(y_label)
    plt.grid(True)
    
    # x축 설정
    plt.xticks(data.iloc[:, 0], rotation=45)
    
    plt.legend()
    plt.show()

# 두 개 데이터의 상관계수를 계산하는 함수
def corr_data(data1, data2):

    # 데이터프레임 병합
    merged_df = pd.DataFrame({
        'data1': data1.iloc[:, 1],
        'data2': data2.iloc[:, 1]
    })
    data1.iloc[:, 0], data2.iloc[:, 1]
    # 상관계수 계산
    correlation = merged_df['data1'].corr(merged_df['data2'])
    
    return correlation

def plot_dual_data(data1, data2, title, y1_label, y2_label):
    # 두 개의 데이터를 하나의 그래프에 그리는 함수
    # 그래프 생성
    fig, ax1 = plt.subplots(figsize=(15, 7))
    
    # 첫 번째 데이터 그래프 (파란색)
    ax1.set_xlabel("연도")
    ax1.set_ylabel(y1_label, color='blue')
    line1 = ax1.plot(range(len(data1)), data1.iloc[:, 1], '-o',
                     color='blue', label=y1_label)
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # x축 눈금 설정
    ax1.set_xticks(range(len(data1)))
    ax1.set_xticklabels(data1.iloc[:, 0], rotation=45)
    
    # 두 번째 데이터 그래프 (빨간색)
    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_label, color='red')
    line2 = ax2.plot(range(len(data2)), data2.iloc[:, 1], '-s',
                     color='red', label=y2_label)
    ax2.tick_params(axis='y', labelcolor='red')
    
    # 그래프 설정
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    # 범례
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.show()

def plot_quad_with_disease(env_data_list, disease_data, titles, env_labels, disease_label, colors):
    """
    4개의 환경 데이터와 하나의 질병 데이터를 2x2 형태로 그리는 함수
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
    axes = [ax1, ax2, ax3, ax4]
    
    # 데이터프레임들의 인덱스를 연도로 설정
    for data in env_data_list:
        if '년' in data.columns:
            data.set_index('년', inplace=True)
        elif '연도' in data.columns:
            data.set_index('연도', inplace=True)
    
    if '년' in disease_data.columns:
        disease_data.set_index('년', inplace=True)
    elif '연도' in disease_data.columns:
        disease_data.set_index('연도', inplace=True)
    
    # 각 서브플롯에 데이터 그리기
    for i, (ax, env_data, title, env_label, color) in enumerate(zip(axes, env_data_list, titles, env_labels, colors)):
        # 환경 데이터의 연도 범위 확인
        start_year = env_data.index.min()
        
        # 해당 연도 범위의 질병 데이터 추출
        disease_data_filtered = disease_data[disease_data.index >= start_year]
        
        # 환경 데이터 그래프 (왼쪽 y축)
        ax.set_xlabel("연도")
        ax.set_ylabel(env_label, color=color)
        line1 = ax.plot(env_data.index, env_data.iloc[:, 0], '-o',
                       color=color, label=env_label, linewidth=2)
        ax.tick_params(axis='y', labelcolor=color)
        
        # 질병 데이터 그래프 (오른쪽 y축)
        ax2 = ax.twinx()
        ax2.set_ylabel(disease_label, color='red')
        line2 = ax2.plot(disease_data_filtered.index, disease_data_filtered.iloc[:, 0], '-s',
                        color='red', label=disease_label, linewidth=2, alpha=0.7)
        ax2.tick_params(axis='y', labelcolor='red')
        
        # x축 설정
        ax.set_xticks(env_data.index)
        ax.tick_params(axis='x', rotation=45)
        
        # 그래프 설정
        ax.set_title(title, pad=20)
        ax.grid(True, alpha=0.3)
        
        # 범례
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    return fig