import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Dashboard():
    def __init__(self, rows=1, cols=1):
        self.rows = rows
        self.cols = cols
        self.fig = make_subplots(
                rows=rows, 
                cols=cols,
                subplot_titles=[' '] * (rows * cols)
        )

    def add_chart(self, x, y, chart_type='line', orientation='v', row=1, col=1, x_label='', y_label='', title='', legend_label='', line=0):

        if chart_type == 'line':
            self.fig.add_trace(
                go.Scatter(x=x, y=y, orientation=orientation, name=legend_label, mode='lines'),
                row=row, col=col,
            )
        elif chart_type == 'bar':
            self.fig.add_trace(
                go.Bar(x=x, y=y, orientation=orientation, name=legend_label),
                row=row, col=col, 
            )

        if line != 0:
            if orientation == 'v':
                self.fig.add_vline(x=line, line_dash="dash", line_color="red", annotation_text=line, row=row, col=col)
            elif orientation == 'h':
                self.fig.add_hline(y=line, line_dash="dash", line_color="red", annotation_text=line, row=row, col=col)

        self.fig.update_xaxes(title_text=x_label, row=row, col=col)
        self.fig.update_yaxes(title_text=y_label, row=row, col=col)
        
        self.fig_idx = (row - 1) * self.cols + (col - 1)
        self.fig.layout.annotations[self.fig_idx].update(text=title)


    def show(self):
        self.fig.update_layout()
        self.fig.show()
