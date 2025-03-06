import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('代码量统计.xlsx')
df.columns = ['week', 'add', 'delete', 'total']
dfmelt = df.melt(id_vars='week')

# 绘制图形
sns.set_theme(style="whitegrid")
g = sns.catplot(
    data=dfmelt, kind="bar",
    x="week", y="value", hue="variable",
    errorbar="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.legend.set_title("")

ax = g.ax
sns.lineplot(data=dfmelt, x="week", y="value", hue="variable", ax=ax, markers=True, dashes=False)
# 关闭图例
ax.legend_.remove()
ax.set_ylabel('')

plt.savefig('code_volume.png')
