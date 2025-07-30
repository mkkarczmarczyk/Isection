import streamlit as st
from sectionproperties.pre.geometry import Geometry 
from sectionproperties.analysis.section import Section 
from sectionproperties.pre.library import i_section
from sectionproperties.pre.library import rectangular_section

import matplotlib.pyplot as plt 

# ──────────────────────────────────────────────────────────────
# Sidebar – user inputs
# ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="I Section Explorer", layout="wide")
st.title("I Section Explorer 🏗️ ")

st.sidebar.header("I Beam Geometry (mm)")
d = st.sidebar.number_input("Height", value=304.0, min_value=100.0, step=1.0)
b = st.sidebar.number_input("Width", value=165.0, min_value=50.0, step=1.0)
t_f=st.sidebar.number_input("Flange thick.", value=10.2, min_value=1.0, step=0.1)
t_w=st.sidebar.number_input("Web thick.", value=6.1, min_value=1.0, step=0.1)
r=st.sidebar.number_input("Root radius", value=11.4, min_value=1.0, step=0.1)


st.sidebar.header("Plate")
d_p = st.sidebar.number_input("Heigth", value=10.0, min_value=10.0,step=1.0)
b_p = st.sidebar.number_input("Width", value=100.0, min_value=10.0, step=1.0)


st.sidebar.header("Bolts")
d_b = st.sidebar.number_input("Bolts dia", value=12.0, min_value=10.0,step=1.0)


# ──────────────────────────────────────────────────────────────
# 1️⃣  Plot section
# ──────────────────────────────────────────────────────────────


ub = i_section(d, b, t_f, t_w, r, n_r=8)
plate= rectangular_section(d_p, b_p)
hole1=rectangular_section(t_f, d_b)
hole2=rectangular_section(d_p, d_b)

plate=plate.align_center(align_to=ub).align_to(other=ub, on="bottom")

dist=0.5*(b-t_w)/2


hole1=hole1.align_center(align_to=ub).align_to(other=ub, on="bottom").shift_section(x_offset=dist)
hole2=hole1.align_center(align_to=ub).align_to(other=ub, on="bottom").shift_section(x_offset=-dist)
hole3=hole2.align_center(align_to=plate).align_to(other=plate, on="top").shift_section(x_offset=dist)
hole4=hole2.align_center(align_to=plate).align_to(other=plate, on="top").shift_section(x_offset=-dist)


geom=ub+plate-hole1-hole2-hole3-hole4


st.subheader("Cross-Section")
fig, ax = plt.subplots()
geom.plot_geometry(ax=ax)  
st.pyplot(fig)           
plt.close(fig)           

# ──────────────────────────────────────────────────────────────
# 2️⃣  Gross Area Properties
# ──────────────────────────────────────────────────────────────


geom.create_mesh(mesh_sizes=[500])
sec = Section(geometry=geom)
sec.calculate_geometric_properties()


zxx_plus, zxx_minus, _, _ = sec.get_z()



st.subheader("Section Modulus")
st.write(f"Zxx+ (top fiber): {zxx_plus:.2f} mm³")
st.write(f"Zxx− (bottom fiber): {zxx_minus:.2f} mm³")



