import tkinter as tk

def create_main_window():
    # create a window
    window = tk.Tk()
    window.title("Network Playground")
    window.geometry("800x600")  # width x height

    # create a canvas for the network visualization
    canvas = tk.Canvas(window, bg="white", width=700, height=500)
    canvas.pack(pady=20)

    # track the nodes and selected node for connection
    nodes = []
    selected_node = None
    selected_text = None

    # function to draw node on canvas
    def draw_node(x, y, node_id):
        radius = 25
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue", outline="black", width=2)
        canvas.create_text(x, y, text=f"Node {node_id}", fill="white", font=("Arial", 10)) 
        nodes.append({"id": node_id, "x": x, "y": y, "connected": []}) 

    def draw_connection(x, y, radius):
        nonlocal selected_node
        for i, node in enumerate(nodes):
                if abs(x - node["x"]) <= radius and abs(y - node["y"]) <= radius:
                    selected = nodes[selected_node]
                    if node["id"] in selected["connected"]:
                        print(f"Nodes {selected['id']} and {node['id']} are already connected")
                        selected_node = None
                        canvas.delete(selected_text)
                        break
                    # draw a line between the selected node and the clicked node
                    canvas.create_line(selected["x"], selected["y"], node["x"], node["y"], fill="black", width=2)
                    # reset selected node
                    selected_node = None
                    # remove the "Selected" text
                    canvas.delete(selected_text)
                    # store the connection
                    selected["connected"].append(node["id"])
                    nodes[i]["connected"].append(selected["id"])
                    print(nodes)
                    break

    # function to draw connection on canvas
    # function to create a node at the clicked position
    def add_node(event):
        nonlocal selected_node
        x, y = event.x, event.y
        node_id = len(nodes) + 1
        radius = 25
        try_draw_node = selected_node is None

        # If no node is selected, create a new node
        if try_draw_node:
            # check if click is inside any existing node (double negative for readability)
            too_close = not all(abs(x - node["x"]) > 50 or abs(y - node["y"]) > 50 for node in nodes)
            if not too_close:
                draw_node(x, y, node_id)
            else:
                print("Node is too close to another node")

        # If a node is selected, draw a connection only if the click is inside a node
        else:
            # try draw connection
            draw_connection(x, y, radius)

    # function to select a node for connecting
    def select_node(event):
        nonlocal selected_node
        nonlocal selected_text
        x, y = event.x, event.y
        for i, node in enumerate(nodes):
            # check if click is inside node's bounds
            if abs(x - node["x"]) <= 25 and abs(y - node["y"]) <= 25:
                if selected_node is None:
                    # select the node
                    selected_node = i
                    selected_text = canvas.create_text(node["x"], node["y"] - 30, text="Selected", fill="red", font=("Arial", 8))
                break

    # bind mouse actions
    canvas.bind("<Button-1>", add_node)  # left-click to add node or connect
    canvas.bind("<Button-3>", select_node)  # right-click to select node

    # start the Tkinter main loop
    window.mainloop()
