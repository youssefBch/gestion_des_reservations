import streamlit as st
import pandas as pd
from connectionDB import *
import streamlit.components.v1 as components
import base64
from headEdite import *

headerEdit()
st.set_page_config(page_title="Welcome To Our Reservation Website", layout="wide", initial_sidebar_state="expanded",page_icon="🏨")
st.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #262730 !important;
    }

    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Header / navbar background */
    header {
        background-color: #0E1117 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ==============================
# FILTERS
# ==============================
st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    type_filter = st.radio(
        "Room type",
        ["All", "Single", "Double", "Suite"]
    )

with col2:
    amenities_filter = st.multiselect(
        "Amenities",
        ["balcony", "jacuzzi", "minibar", "pay-tv"]
    )
spaces_filter = []
with col3:
    # Trois checkboxes séparées pour les espaces
    st.write("Spaces")
    kitchen_checkbox = st.checkbox("Kitchen", value=False)
    bathroom_checkbox = st.checkbox("Bathroom", value=False)
    dining_room_checkbox = st.checkbox("Dining room", value=False)


    if kitchen_checkbox:
        spaces_filter.append("kitchen")
    if bathroom_checkbox:
        spaces_filter.append("bathroom")
    if dining_room_checkbox:
        spaces_filter.append("dining room")


df_filtered = conn.query(f"""
    SELECT CodR, Floor, SurfaceArea, Type
    FROM ROOM
""")

# Initialize default values for filters
radioSelected = ('suite', 'double', 'single')

# Filter by room type
if type_filter != "All":
    radioSelected = f"('{type_filter.lower()}')"
    df_filtered = conn.query(f"""
        SELECT CodR, Floor, SurfaceArea, Type
        FROM ROOM
        WHERE Type IN {radioSelected};
    """)

# Filter by amenities
selected_amenities = ("balcony", "jacuzzi", "minibar", "pay-tv")

if amenities_filter:
    selected_amenities = tuple(amenities_filter)
    if len(selected_amenities) == 1:
        selected_amenities = f"('{selected_amenities[0]}')"
        countSelected = 1
    else:
        countSelected = len(selected_amenities)

    # Build query based on spaces filters
    if spaces_filter:
        # Case: Amenities + Spaces filters
        spaces_selected = tuple(spaces_filter)
        if len(spaces_selected) == 1:
            spaces_selected = f"('{spaces_selected[0]}')"
            spaces_count = 1
        else:
            spaces_count = len(spaces_selected)

        # Query with amenities and spaces
        df_filtered = conn.query(f"""
            SELECT amenities.CodR, amenities.Floor, amenities.SurfaceArea, amenities.Type
            FROM (
                SELECT r.CodR, r.Floor, r.SurfaceArea, r.Type, COUNT(DISTINCT ha.AMENITIES_Amenity) as amenity_count
                FROM ROOM r
                JOIN HAS_AMENITIES ha ON ha.ROOM_CodR = r.CodR
                WHERE r.Type IN {radioSelected}
                AND ha.AMENITIES_Amenity IN {selected_amenities}
                GROUP BY r.CodR, r.Floor, r.SurfaceArea, r.Type
                HAVING amenity_count = {countSelected}
            ) amenities
            WHERE amenities.CodR IN (
                SELECT r.CodR
                FROM ROOM r
                JOIN HAS_SPACES hs ON hs.ROOM_CodR = r.CodR
                WHERE r.Type IN {radioSelected}
                AND hs.SPACES_Space IN {spaces_selected}
                GROUP BY r.CodR
                HAVING COUNT(DISTINCT hs.SPACES_Space) = {spaces_count}
            )
        """)
    else:
        # Case: Amenities filter only
        df_filtered = conn.query(f"""
            SELECT r.CodR, r.Floor, r.SurfaceArea, r.Type
            FROM ROOM r
            JOIN HAS_AMENITIES ha ON ha.ROOM_CodR = r.CodR
            WHERE r.Type IN {radioSelected}
            AND ha.AMENITIES_Amenity IN {selected_amenities}
            GROUP BY r.CodR, r.Floor, r.SurfaceArea, r.Type
            HAVING COUNT(DISTINCT ha.AMENITIES_Amenity) = {countSelected};
        """)
elif spaces_filter:
    # Case: Spaces filter only (without amenities)
    spaces_selected = tuple(spaces_filter)
    if len(spaces_selected) == 1:
        spaces_selected = f"('{spaces_selected[0]}')"
        spaces_count = 1
    else:
        spaces_count = len(spaces_selected)

    df_filtered = conn.query(f"""
        SELECT r.CodR, r.Floor, r.SurfaceArea, r.Type
        FROM ROOM r
        JOIN HAS_SPACES hs ON hs.ROOM_CodR = r.CodR
        WHERE r.Type IN {radioSelected}
        AND hs.SPACES_Space IN {spaces_selected}
        GROUP BY r.CodR, r.Floor, r.SurfaceArea, r.Type
        HAVING COUNT(DISTINCT hs.SPACES_Space) = {spaces_count};
    """)

# ==============================
# DISPLAY TABLE
# ==============================
st.subheader("Available Rooms (Table)")

# Display all columns with English headers
df_display = df_filtered.copy()
df_display = df_display.rename(columns={
    'CodR': 'Room Code',
    'Floor': 'Floor',
    'SurfaceArea': 'Area (m²)',
    'Type': 'Type'
})

st.dataframe(
    df_display,
    use_container_width=True
)


def room_card(room_code, floor, area, room_type):
    st.html("""
    <style>
        .property-card{
            border: 1px solid #ffffff21;
            display: flex;
            align-items: flex-start;
            width:100%;            
            height: 350px;
            border-radius:16px;
            overflow:hidden;
            box-shadow: 0 10px 30px rgba(20,30,70,0.08);
            transition:transform .25s ease, box-shadow .25s ease;
            justify-content: center;
        }
        .property-card:hover{
            transform:translateY(-8px);
            box-shadow: 0 20px 50px rgba(20,30,70,0.12);
        }
        .property-card:hover:before{
            transform: scale(2);
            height: 7px;
            border-radius: 50%;
        }
        .property-card:before {
            content: "";
            position: absolute;
            background-color: #b8962e;
            position: absolute;
            width: 100%;
            height: 0px;
            bottom: 0px;
            right: 0px;
            opacity: 0.9;
            border-radius: 0%;
            transform: scale(0);
            transition: all 0.4s linear 0s;
        }
        .card-body{
            padding:18px;
        }
        .card-body .title{
            margin: 0 0 8px 0;
            margin-top:5px;
            font-size: 18px;
            color: var(--muted);
        }
        .meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 14px;
        }
        .meta-item {
            display: flex;
            justify-content: space-between;
        }
        .card-image{
            width:100%;
            height: 180px;
            object-fit: cover;
            border-radius: 5px;
        }
    </style>
    """)

    if room_type == "suite":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg6.jpg")}" style="width:100%">'
    elif room_type == "double":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg7.jpg")}" style="width:100%">'
    elif room_type == "single":
        image_html = f'<img class="card-image" src="data:image/png;base64,{img_to_base64("assets/bg9.jpg")}" style="width:100%">'

    st.html(f"""
        <div class="property-card">
            <div class="card-body">
                {image_html}
                <h3 class="title">Room {room_code}</h3>
                <div class="meta">
                    <div class="meta-item">
                        <span>Floor:</span>
                        <span>{floor}</span>
                    </div>
                    <div class="meta-item">
                        <span>Area:</span>
                        <span>{area} m²</span>
                    </div>
                    <div class="meta-item">
                        <span>Type:</span>
                        <span>{room_type}</span>
                    </div>
                </div>
            </div>
        </div>
    """)


# Display room cards
st.subheader("Available Rooms (Cards)")

cols = st.columns(3)
i = 0
for index, row in df_filtered.iterrows():
    with cols[i]:
        room_card(row["CodR"], row["Floor"], row["SurfaceArea"], row["Type"])
    if i == 2:
        i = 0
    else:
        i = i + 1