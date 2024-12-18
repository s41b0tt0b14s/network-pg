import tkinter as tk

def create_main_window():
    # create a window
    window = tk.Tk()
    window.title("Network Playground")
    window.geometry("800x600")  # width x height

    NODE_TYPES ={
        "router": {"color": "green", "shape": "rectangle"},
        "switch": {"color": "orange", "shape": "oval"},
        "user": {"color": "blue", "shape": "circle"}
    }

    # create a canvas for the network visualization
    canvas = tk.Canvas(window, bg="white", width=700, height=500)
    canvas.pack(pady=20)

    # track the nodes and selected node for connection
    nodes = []
    selected_node = None
    selected_text = None
    running_node_id = 0
    show_context_menu_event_x = None
    show_context_menu_event_y = None
    drawn_node_id = []
    drawn_text_id = []
    connection_selecting_flag = False

    def show_context_menu(event):
        nonlocal selected_node, show_context_menu_event_x, show_context_menu_event_y, selected_text, connection_selecting_flag
        show_context_menu_event_x, show_context_menu_event_y = event.x, event.y
        for i, node in enumerate(nodes):
            if abs(show_context_menu_event_x - node["x"]) <= 25 and abs(show_context_menu_event_y - node["y"]) <= 25:
                selected_node = i
                context_menu.post(event.x_root, event.y_root)
                break
        selected_node = None
        connection_selecting_flag = False
        canvas.delete(selected_text)

    # function to draw node on canvas
    def draw_node(x, y, node_id, node_type="user"):
        radius = 25
        node_properties = NODE_TYPES[node_type]
        
        # Draw node based on its type
        if node_properties["shape"] == "rectangle":
            shape_id = canvas.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=node_properties["color"], outline="black", width=2)
        elif node_properties["shape"] == "oval":
            shape_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=node_properties["color"], outline="black", width=2)
        else:
            shape_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=node_properties["color"], outline="black", width=2)
        
        # Draw the node's label
        text_id = canvas.create_text(x, y, text=f"{node_type.title()} {node_id}", fill="white", font=("Arial", 10)) 
        
        drawn_node_id.append(shape_id)
        drawn_text_id.append(text_id)
        nodes.append({"id": node_id, "x": x, "y": y, "shape_id": shape_id, "text_id": text_id, "type": node_type, "drawn_connections_ids":[], "connected": []}) 

    def create_node_type_menu():
        node_type_menu = tk.Menu(context_menu, tearoff=0)
        node_type_menu.add_command(label="Router", command=lambda: add_node("router"))
        node_type_menu.add_command(label="Switch", command=lambda: add_node("switch"))
        node_type_menu.add_command(label="User", command=lambda: add_node("user"))
        return node_type_menu

    def draw_connection(x, y, radius):
        nonlocal selected_node, connection_selecting_flag
        for i, node in enumerate(nodes):
                if abs(x - node["x"]) <= radius and abs(y - node["y"]) <= radius and selected_text is not None:
                    selected = nodes[selected_node]
                    already_connected = node["id"] in selected["connected"]
                    self_connected = selected["id"] == node["id"]
                    if already_connected:
                        print(f"Nodes {selected['id']} and {node['id']} are already connected")
                        selected_node = None
                        connection_selecting_flag = False
                        canvas.delete(selected_text)
                        break
                    elif self_connected:
                        print("Cannot connect a node to itself")
                        selected_node = None
                        connection_selecting_flag = False
                        canvas.delete(selected_text)
                        break
                    # draw a line between the selected node and the clicked node
                    drawn_line = canvas.create_line(selected["x"], selected["y"], node["x"], node["y"], fill="black", width=2)
                    canvas.tag_lower(drawn_line)  # send line to back
                    # reset selected node
                    selected_node = None
                    # remove the "Selected" text
                    connection_selecting_flag = False
                    canvas.delete(selected_text)
                    # store the connection
                    selected["connected"].append(node["id"])
                    nodes[i]["connected"].append(selected["id"])
                    selected["drawn_connections_ids"].append(drawn_line)
                    nodes[i]["drawn_connections_ids"].append(drawn_line)
                    for i in nodes:
                        print(i)
                    break

    # helper for add_node to handle logic unrelated to actually drawing
    def add_node_helper(x, y, node_id, radius, is_new_node_click, node_type):
        nonlocal running_node_id
        # if no node is selected, create a new node
        if is_new_node_click and not connection_selecting_flag:
            # check if the desired new node is too close to another existing node
            too_close = not all(abs(x - node["x"]) > 50 or abs(y - node["y"]) > 50 for node in nodes)
            if not too_close:
                draw_node(x, y, node_id, node_type)
                running_node_id += 1
            else:
                print(f"Node {node_id} is too close")
        # if a node is already selected, connect the selected node to the clicked node
        else:
            draw_connection(x, y, radius)

    # function to create a node at the clicked position
    def add_node(node_type):
        nonlocal selected_node
        x, y = show_context_menu_event_x, show_context_menu_event_y
        node_id = running_node_id
        radius = 25
        is_new_node_click = selected_node is None

        add_node_helper(x, y, node_id, radius, is_new_node_click, node_type)

    # function to select a node for connecting
    def select_node():
        nonlocal selected_node, selected_text, show_context_menu_event_x, show_context_menu_event_y, connection_selecting_flag
        x, y = show_context_menu_event_x, show_context_menu_event_y
        for i, node in enumerate(nodes):
            # check if click is inside node's bounds
            if abs(x - node["x"]) <= 25 and abs(y - node["y"]) <= 25:
                if selected_node is None:
                    # select the node
                    print(f"Selected node {node['id']}")
                    selected_node = i
                    connection_selecting_flag = True
                    selected_text = canvas.create_text(node["x"], node["y"] - 30, text="Selected", fill="red", font=("Arial", 8))
                break

    def delete_node():
        nonlocal selected_node
        removed_line_ids = []
        for i, node in enumerate(nodes):
            if abs(show_context_menu_event_x - node["x"]) <= 25 and abs(show_context_menu_event_y - node["y"]) <= 25:
                selected_node = i
                break
        if selected_node is not None:
            node = nodes[selected_node]
            canvas.delete(node["shape_id"])
            canvas.delete(node["text_id"])
            nodes.pop(selected_node)
            for line_id in node["drawn_connections_ids"]:
                removed_line_ids.append(line_id)
                canvas.delete(line_id)
            for connected_node_id in node["connected"]:
                for i, connected_node in enumerate(nodes):
                    if connected_node["id"] == connected_node_id:
                        connected_node["connected"].remove(node["id"])
                        for line_id in connected_node["drawn_connections_ids"]:
                            if line_id in removed_line_ids:
                                connected_node["drawn_connections_ids"].remove(line_id)
        selected_node = None
            
    def show_node_type_menu(event):
        nonlocal show_context_menu_event_x, show_context_menu_event_y, connection_selecting_flag, selected_node
        if not connection_selecting_flag:
            show_context_menu_event_x, show_context_menu_event_y = event.x, event.y
            node_type_menu = create_node_type_menu()
            node_type_menu.post(event.x_root, event.y_root)
        else:
            for i, node in enumerate(nodes):
                if abs(event.x - node["x"]) <= 25 and abs(event.y - node["y"]) <= 25:
                    selected_node = i
                    break
            add_node("user")

    # create a context menu
    context_menu = tk.Menu(window, tearoff=0)
    context_menu.add_cascade(label="Node Type", menu=create_node_type_menu())
    context_menu.add_command(label="Delete Node", command=delete_node)
    context_menu.add_command(label="Connect Node", command=select_node)
    
    # bind mouse actions
    canvas.bind("<Button-1>", show_node_type_menu)  # left-click to add node or connect
    
    canvas.bind("<Button-3>", show_context_menu)  # right-click to select node

    # start the Tkinter main loop
    window.mainloop() 