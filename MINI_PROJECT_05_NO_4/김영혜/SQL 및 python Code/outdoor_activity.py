# [1] [모듈 및 데이터 로딩]
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from tabulate import tabulate
import seaborn as sns
import numpy as np

# MySQL 연결 함수
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        user="emily0",
        password="1234",
        db="leisure",
        charset="utf8"
    )
    return conn

# MySQL에서 데이터를 가져와 DataFrame으로 변환하는 함수
def fetch_data(query):
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    cur.close()
    conn.close()
    return df

#-----------------------------------------------------------------------------------
# 1. 2013년부터 각 경제지표(4가지) 변화
# 4가지 경제지표 dataframe 만드는 함수
def get_economy_data(table_name):
    query = f"""
    SELECT year, 전국, 서울특별시, 부산광역시, 대구광역시, 
                  인천광역시, 광주광역시, 대전광역시, 울산광역시
    FROM {table_name}
    WHERE year >= 2013
    ORDER BY year
    """
    return fetch_data(query)

# 고용율, 실업률, 경제활동인구비율, 비경제활동인구수 df 만들기
df_employment_rate = get_economy_data("employment_data")  # 고용률
df_unemployment_rate = get_economy_data("unemployment_data")  # 실업률
df_active_population = get_economy_data("active_economy_data")  # 경제활동인구
df_inactive_population = get_economy_data("inactive_economy_data")  # 비경제활동인구

def get_economy_summary_data():
    query = """
    SELECT *
    FROM income_impacts
    """
    return fetch_data(query)
ecomomy_summary = get_economy_summary_data()

# 2. 경제지표 없이 outdoor_activity 지표들 따로 보여주는 2가지
# 2-1. 놀이공원 이용객 수
def get_park_data():
    query = """
    SELECT year, 롯데월드, 이월드, 서울랜드, 에버랜드, 경주월드, 
           (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
    FROM park_fixed
    ORDER BY year
    """
    return fetch_data(query)

df_park = get_park_data()

# 2-2. 전국 관광지점수 및 관광이용객수
def get_tour_data():
    query = """
    SELECT *
    FROM tour_fixed
    ORDER BY year
    """
    return fetch_data(query)

df_tour = get_tour_data()

# 3. outdoor_activity 지표들(4가지)과 경제지표(비경제활동인구수, 실업률)
# 3-1. 전국 스키장이용객수와 경제지표
def get_ski_economy_data():
    query = """
    SELECT s.year, s.스키_이용객_수, 
           e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
    FROM ski_fixed s
    INNER JOIN economic_summary e ON s.year = e.year
    ORDER BY s.year
    """
    return fetch_data(query)

df_ski_economy = get_ski_economy_data()

# 3-2 전국 관광입장객수와 경제지표
def get_tour_economy_data():
    query = """
    SELECT t.year, t.입장객_수, 
           e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
    FROM tour_fixed t
    INNER JOIN economic_summary e ON t.year = e.year
    ORDER BY t.year
    """
    return fetch_data(query)

df_tour_economy = get_tour_economy_data()

# 3-3 놀이공원 총 이용객수와 경제지표
def get_park_economy_data():
    query = """
    SELECT p.year,p.전체_이용객수,
        e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
    FROM (
        SELECT year,
               (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
        FROM park_fixed
    ) p
    INNER JOIN economic_summary e ON p.year = e.year
    ORDER BY p.year
    """
    return fetch_data(query)

df_park_economy = get_park_economy_data()

# 3-4. 전국 온천이용객 수와 경제지표
def get_hotspring_economy_data():
    query = """
    SELECT h.year, h.전국 AS 전국_온천_이용객, e.active_population AS 경제활동인구, 
           e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
    FROM hotspring_data h
    INNER JOIN economic_summary e ON h.year = e.year
    ORDER BY h.year
    """
    return fetch_data(query)

df_hotspring_economy = get_hotspring_economy_data()

# 4. 기타 dataframe
# 4-1. 설문조사 df
def get_incomeimpact_data():
    query = """
    SELECT *
    FROM income_impacts
    """
    return fetch_data(query)

df_income_impact = get_incomeimpact_data()

# 4-2 상관계수 heatmap을 위한 전체 4개 경제지표와 4개 여가활동지표 df
def get_correlation_data():
    query = """
    SELECT e.year,
           e.전국 AS 고용률,
           u.전국 AS 실업률,
           a.전국 AS 경제활동인구비율,
           i.전국 AS 비경제활동인구수,
           p.전체_이용객수 AS 놀이공원_이용객,
           h.전국 AS 온천_이용객,
           s.스키_이용객_수 AS 스키장_이용객,
           t.입장객_수 AS 관광_입장객
    FROM employment_data e
    INNER JOIN unemployment_data u ON e.year = u.year
    INNER JOIN active_economy_data a ON e.year = a.year
    INNER JOIN inactive_economy_data i ON e.year = i.year
    INNER JOIN (
        SELECT year, (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
        FROM park_fixed
    ) p ON e.year = p.year
    INNER JOIN hotspring_data h ON e.year = h.year
    INNER JOIN ski_fixed s ON e.year = s.year
    INNER JOIN tour_fixed t ON e.year = t.year
    ORDER BY e.year;
    """
    return fetch_data(query)

df_correlation = get_correlation_data()

#--------------------------------------------------------------------------------------
# [데이터시각화]
"""
1. 각 경제지표 4가지 각각 그래프 만들기 -> 총 4개가 나올것임
2. 2-1~2-3까지 3가지 dataframe과 3-1(ski) dataframe -> 총 4개 그래프
4. 4-1로 설문조사 dataframe pie 그래프 그리기, 4-2로 heatmap 그리기
3. 3-1 ~ 3-4 총 4가지 dataframe에서 subplot이 4개. 각 subplot에서는 비경제활동인구수와 해당활동지표, 실업율과 해당활동지표 회귀추세선 그리기
"""
# 색상 코드
color1=plt.cm.Paired.colors
color2=['#233d4d','#fe7f2d','#fcca46','#a1c181','#619b8a']

# 1-1. 각 경제지표 그래프
plt.figure(figsize=(14, 10))

df_list = [df_employment_rate, df_unemployment_rate, df_active_population, df_inactive_population]
titles = ["고용률 변화", "실업률 변화", "경제활동인구비율 변화", "비경제활동인구수 변화"]
y_labels = ["고용률 (%)", "실업률 (%)", "경제활동인구비율 (%)", "비경제활동인구수 (천 명)"]

for i, df in enumerate(df_list):
    plt.subplot(2, 2, i+1)
    for j, col in enumerate(df.columns[1:]):  # 컬럼 루프는 한 번만 사용 -> 안그럼 무한루프됨....
        plt.plot(df["year"], df[col], marker="o", label=col, color=color1[j % len(color1)])  
    plt.title(titles[i])
    plt.xlabel("년도")
    plt.ylabel(y_labels[i])
    plt.legend()

plt.suptitle("경제지표(주요도시)", fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()


# 1-2. 경제지표 4가지 (전국만 비교)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

df_list = [df_employment_rate, df_unemployment_rate, df_active_population, df_inactive_population]
titles = ["고용률 변화 (전국)", "실업률 변화 (전국)", "경제활동인구비율 변화 (전국)", "비경제활동인구수 변화 (전국)"]
y_labels = ["고용률 (%)", "실업률 (%)", "경제활동인구비율 (%)", "비경제활동인구수 (천 명)"]

for i, df in enumerate(df_list):
    ax = axes[i // 2, i % 2]
    ax.plot(df["year"], df["전국"], marker="o", color=color2[i], label="전국")
    ax.set_title(titles[i])
    ax.set_xlabel("년도")
    ax.set_ylabel(y_labels[i])
    ax.legend()

plt.suptitle("경제지표(전국)", fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------------------
# 2. 여가 활동 지표 그래프
# 전국 이용객수 그래프 & 놀이공원은 개별과 전체 다 나타내기
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# (1) 관광지 입장객 수 & 관광지점 수 (막대 + 꺾은선 그래프)
ax1 = axes[0, 0]
ax2 = ax1.twinx()

ax1.bar(df_tour["year"], df_tour["관광지점_수"], color="#74a9cf", alpha=0.7, label="관광지점 수")
ax2.plot(df_tour["year"], df_tour["입장객_수"], marker="o", color=color2[1], label="관광 입장객 수")

ax1.set_xlabel("년도")
ax1.set_ylabel("관광지점 수", color="#74a9cf")
ax2.set_ylabel("입장객 수", color=color2[1])
ax1.set_title("관광지점 수 & 관광 입장객 수 변화")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# (2) 온천 이용객 (전국만)
axes[0, 1].plot(df_hotspring_economy["year"], df_hotspring_economy["전국_온천_이용객"], marker="o", color=color2[0], label="전국")
axes[0, 1].set_title("온천 이용객 변화 (전국)")
axes[0, 1].set_xlabel("년도")
axes[0, 1].set_ylabel("이용객 수")
axes[0, 1].legend()

# (3) 놀이공원 이용객 (개별 놀이공원 + 전체 이용객)
for j, col in enumerate(df_park.columns[1:]):  # 'year' 제외
    axes[1, 0].plot(df_park["year"], df_park[col], marker="o", label=col, color=color1[j % len(color1)])

axes[1, 0].set_title("놀이공원 이용객 변화")
axes[1, 0].set_xlabel("년도")
axes[1, 0].set_ylabel("이용객 수")
axes[1, 0].legend()

# (4) 스키장 이용객 (스키 이용객만)
axes[1, 1].plot(df_ski_economy["year"], df_ski_economy["스키_이용객_수"], marker="o", color=color2[3], label="스키장 이용객")
axes[1, 1].set_title("스키장 이용객 변화")
axes[1, 1].set_xlabel("년도")
axes[1, 1].set_ylabel("이용객 수")
axes[1, 1].legend()

plt.suptitle("아웃도어 여가활동 변화", fontsize=20, fontweight="bold",y=1.)
plt.tight_layout()
plt.show()
#---------------------------------------------------------
# 4-1 설문조사 pie 그래프
# 소득 분위 리스트 (소계 포함)
income_brackets = df_income_impact.index  
num_brackets = len(income_brackets)

# 한 줄에 4개씩 배치 (자동 계산)
num_cols = 4
num_rows = (num_brackets + num_cols - 1) // num_cols  # 올림처리하여 행 개수 계산

# 소득 분위별 Pie 차트 그리기 (Legend 포함)
# [1] 인덱스 설정 오류 수정
df_income_impact.set_index("소득별", inplace=True)

# [2] 소득 분위 리스트 가져오기
income_brackets = df_income_impact.index.tolist()

# [3] Pie 차트 그리기
fig, axes = plt.subplots(2, 4, figsize=(16, 10))  # 한 줄에 4개씩 배치

axes = axes.flatten()
legend_labels = df_income_impact.columns  # 응답 카테고리 리스트

for i, income in enumerate(income_brackets):
    wedges, texts, autotexts = axes[i].pie(
        df_income_impact.loc[income],
        autopct=lambda p: f'{p:.1f}%' if p > 2 else '',  # 2% 이하 값 생략
        startangle=90,
        pctdistance=1.2,
        colors=color1,
        shadow=True
    )

    axes[i].set_title(f"{income} 여가생활 영향")
    axes[i].set_ylabel("")

fig.legend(legend_labels, title="설문 응답", loc="upper right", bbox_to_anchor=(1.05, 1))

plt.suptitle("소득별 여가생활 영향 분석", fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()


# 4-2 경제-여가 활동 상관관계 히트맵
plt.figure(figsize=(10, 8))

# 상관행렬 계산 (year 컬럼 제외)
correlation_matrix = df_correlation.drop(columns=["year"]).corr()

# 상삼각행렬을 제거하기 위한 마스크 생성
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

# 히트맵 그리기 (위쪽 삼각형 제거)
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    linewidths=0.5, 
    mask=mask  # 마스킹 적용
)

# X축, Y축 라벨 회전 (X축 45도 회전)
plt.xticks(rotation=45)
plt.yticks(rotation=0)  # Y축은 그대로 유지

plt.title("경제지표 & 여가활동 상관관계",fontsize=20, fontweight="bold")
plt.show()
#-----------------------------------------------------------------------------
# 3. 비경제활동인구 & 실업률 vs. 여가활동 subplot (8개 그래프) 회귀선
fig, axes = plt.subplots(4, 2, figsize=(14, 20))

df_list = [df_ski_economy, df_tour_economy, df_park_economy, df_hotspring_economy]
titles = ["스키장 이용객", "관광 입장객", "놀이공원 이용객", "온천 이용객"]
y_labels = ["이용객 수 (천 명)", "이용객 수 (천 명)", "이용객 수 (천 명)", "이용객 수 (천 명)"]

for i, df in enumerate(df_list):
    # (1) 비경제활동인구 vs 활동지표
    ax1 = axes[i, 0]
    sns.regplot(x=df["비경제활동인구"], y=df.iloc[:, 1], ax=ax1, scatter_kws={"s": 50}, color="deepskyblue")
    ax1.set_title(f"{titles[i]} vs. 비경제활동인구")
    ax1.set_xlabel("비경제활동인구 (천 명)")
    ax1.set_ylabel(y_labels[i])

    # (2) 실업률 vs 활동지표
    ax2 = axes[i, 1]
    sns.regplot(x=df["실업률"], y=df.iloc[:, 1], ax=ax2, scatter_kws={"s": 50}, color="dodgerblue")
    ax2.set_title(f"{titles[i]} vs. 실업률")
    ax2.set_xlabel("실업률 (%)")
    ax2.set_ylabel(y_labels[i])

plt.suptitle("아웃도어 여가활동과 경제지표 비교",fontsize=20, fontweight="bold",y=1.)
plt.tight_layout()
plt.show()

# 지역이 있는 데이터는 '전국'만 그린 그래프를 발표에 사용하기 -> 주요도시로 추렸는데도 그래프가 지저분함...