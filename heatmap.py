# ============================================================
#  Multi-Heatmap Visualization App
# ============================================================

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import io

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from scipy.spatial.distance import pdist, squareform

# ============================================================
# Page Config
# ============================================================

st.set_page_config(layout="wide")
st.title(" Multi-Heatmap Visualization App")

# ============================================================
# File Upload
# ============================================================

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.error("At least two numeric columns are required.")
        st.stop()

    # ============================================================
    # Sidebar – Global Settings
    # ============================================================

    st.sidebar.header("Global Data Settings")

    selected_cols = st.sidebar.multiselect(
        "Select numeric columns",
        numeric_cols,
        default=numeric_cols
    )

    scaling = st.sidebar.selectbox(
        "Scaling method",
        ["None", "Z-score", "Min-Max"]
    )

    data = df[selected_cols].dropna()

    if scaling == "Z-score":
        data = pd.DataFrame(StandardScaler().fit_transform(data), columns=data.columns)
    elif scaling == "Min-Max":
        data = pd.DataFrame(MinMaxScaler().fit_transform(data), columns=data.columns)

    # ============================================================
    # Sidebar – Figure Formatting (Journal Grade)
    # ============================================================

    st.sidebar.header("Figure Formatting")

    fig_width = st.sidebar.slider("Figure width (inches)", 6, 20, 10)
    fig_height = st.sidebar.slider("Figure height (inches)", 4, 15, 8)

    dpi = st.sidebar.selectbox("Export DPI", [300, 600])

    font_family = st.sidebar.selectbox(
        "Font family",
        ["Times New Roman", "Arial", "Helvetica"]
    )

    base_font = st.sidebar.slider("Base font size", 8, 20, 12)

    cmap = st.sidebar.selectbox(
        "Color map",
        ["viridis", "coolwarm", "magma", "Blues", "Greens"]
    )

    plt.rcParams.update({
        "font.family": font_family,
        "font.size": base_font
    })

    # ============================================================
    # Heatmap Selection
    # ============================================================

    heatmap_type = st.selectbox(
        "Select Heatmap Type",
        [
            "Correlation",
            "Clustered (Hierarchical)",
            "Distance Matrix",
            "Density (2D)",
            "Confusion Matrix"
        ]
    )

    fig = None
    methods_text = []

    # ============================================================
    # CORRELATION HEATMAP
    # ============================================================

    if heatmap_type == "Correlation":
        method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"])
        mask_upper = st.checkbox("Mask upper triangle", value=True)

        corr = data.corr(method=method)
        mask = np.triu(np.ones_like(corr, dtype=bool)) if mask_upper else None

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        sns.heatmap(corr, mask=mask, cmap=cmap, square=True, linewidths=0.5, ax=ax)

        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)

        methods_text.append(
            f"{method.capitalize()} correlation heatmap generated using "
            f"{scaling if scaling != 'None' else 'unscaled'} variables."
        )

    # ============================================================
    # CLUSTERED HEATMAP
    # ============================================================

    elif heatmap_type == "Clustered (Hierarchical)":
        linkage_method = st.selectbox(
            "Linkage method", ["average", "complete", "single", "ward"]
        )
        metric = st.selectbox(
            "Distance metric", ["euclidean", "correlation", "cosine"]
        )

        corr = data.corr()

        cg = sns.clustermap(
            corr,
            cmap=cmap,
            linewidths=0.5,
            figsize=(fig_width, fig_height),
            method=linkage_method,
            metric=metric
        )

        st.pyplot(cg.fig)
        fig = cg.fig

        methods_text.append(
            f"Hierarchical clustering applied using {linkage_method} linkage "
            f"and {metric} distance on correlation matrix."
        )

    # ============================================================
    # DISTANCE MATRIX
    # ============================================================

    elif heatmap_type == "Distance Matrix":
        metric = st.selectbox("Distance metric", ["euclidean", "cityblock", "cosine"])

        if data.shape[0] > 800:
            st.warning("Large dataset detected. Distance matrix may be slow.")

        dist = squareform(pdist(data.values, metric=metric))
        dist_df = pd.DataFrame(dist, index=data.index, columns=data.index)

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        sns.heatmap(dist_df, cmap=cmap, ax=ax)
        ax.set_title("Distance Matrix Heatmap")
        st.pyplot(fig)

        methods_text.append(
            f"Distance matrix computed using {metric} distance."
        )

    # ============================================================
    # DENSITY HEATMAP
    # ============================================================

    elif heatmap_type == "Density (2D)":
        x = st.selectbox("X-axis variable", selected_cols)
        y = st.selectbox("Y-axis variable", selected_cols, index=1)

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        sns.kdeplot(x=data[x], y=data[y], fill=True, cmap=cmap, ax=ax)

        ax.set_title(f"2D Density Heatmap: {x} vs {y}")
        st.pyplot(fig)

        methods_text.append(
            f"2D kernel density estimation performed for variables {x} and {y}."
        )

    # ============================================================
    # CONFUSION MATRIX
    # ============================================================

    elif heatmap_type == "Confusion Matrix":
        y_true_col = st.selectbox("True label column", df.columns)
        y_pred_col = st.selectbox("Predicted label column", df.columns)

        normalize = st.checkbox("Normalize", value=False)

        y_true = df[y_true_col]
        y_pred = df[y_pred_col]

        cm = confusion_matrix(y_true, y_pred)
        if normalize:
            cm = cm / cm.sum(axis=1, keepdims=True)

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        sns.heatmap(
            cm,
            annot=True,
            fmt=".2f" if normalize else "d",
            cmap=cmap,
            ax=ax
        )

        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average="macro", zero_division=0)
        rec = recall_score(y_true, y_pred, average="macro", zero_division=0)

        ax.set_title(f"Confusion Matrix (Acc={acc:.2f})")
        st.pyplot(fig)

        methods_text.append(
            f"Confusion matrix generated with accuracy={acc:.2f}, "
            f"macro-precision={prec:.2f}, macro-recall={rec:.2f}."
        )

    # ============================================================
    # EXPORT FIGURES
    # ============================================================

    if fig:
        st.subheader("Export Figure")

        buf_png = io.BytesIO()
        fig.savefig(buf_png, format="png", dpi=dpi, bbox_inches="tight")
        st.download_button(
            "Download PNG",
            buf_png.getvalue(),
            file_name="figure.png",
            mime="image/png"
        )

        buf_pdf = io.BytesIO()
        fig.savefig(buf_pdf, format="pdf", bbox_inches="tight")
        st.download_button(
            "Download PDF",
            buf_pdf.getvalue(),
            file_name="figure.pdf",
            mime="application/pdf"
        )

        buf_svg = io.BytesIO()
        fig.savefig(buf_svg, format="svg", bbox_inches="tight")
        st.download_button(
            "Download SVG",
            buf_svg.getvalue(),
            file_name="figure.svg",
            mime="image/svg+xml"
        )

    # ============================================================
    # METHODS / REPRODUCIBILITY BLOCK
    # ============================================================

    st.subheader("Methods (Copy for Manuscript)")

    methods_block = (
        "Heatmaps were generated using a Streamlit-based visualization tool. "
        + " ".join(methods_text)
        + f" Figures were exported at {dpi} DPI using the {font_family} font."
    )

    st.text_area("Methods text", methods_block, height=150)

    st.download_button(
        "Download Methods Text",
        methods_block,
        file_name="methods.txt"
    )

    # ============================================================
    # SETTINGS EXPORT
    # ============================================================

    settings = {
        "columns": selected_cols,
        "scaling": scaling,
        "heatmap_type": heatmap_type,
        "colormap": cmap,
        "figure_size": [fig_width, fig_height],
        "dpi": dpi,
        "font": font_family
    }

    st.download_button(
        "Download Analysis Settings (JSON)",
        data=json.dumps(settings, indent=2),
        file_name="analysis_settings.json",
        mime="application/json"
    )
