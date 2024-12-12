from tkinter import Tk, Label, Entry, Button, ttk

class NextFitMemoryAllocation:
    def __init__(self, root):
        self.root = root
        self.root.title("Next Fit Memory Allocation")

        # Define memory blocks (Block number, Total Size, Free Size)
        self.memory_blocks = [{"Block No": i+1, "Size": size, "Free": size, "Used": 0, "Process": {}, "Job Sizes": {}} for i, size in enumerate([20, 10, 30, 50, 15])]
        self.allocation_pointer = 0

        # UI Layout
        left_frame = ttk.Frame(root)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        right_frame = ttk.Frame(root)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Left side - Name input and complete button
        self.job_name_label = Label(left_frame, text="Job Name:")
        self.job_name_label.grid(row=0, column=0, pady=5)

        self.job_name_entry = Entry(left_frame)
        self.job_name_entry.grid(row=1, column=0, pady=5)

        self.complete_button = Button(left_frame, text="Complete Job", command=self.complete_job)
        self.complete_button.grid(row=2, column=0, pady=5)

        # Right side - Job size input and submit button
        Label(right_frame, text="Job Size (KB):").grid(row=0, column=0, pady=5)
        self.job_size_entry = Entry(right_frame)
        self.job_size_entry.grid(row=1, column=0, pady=5)

        self.submit_button = Button(right_frame, text="Submit Job", command=self.add_job)
        self.submit_button.grid(row=2, column=0, pady=5)

        # Memory status table
        self.tree = ttk.Treeview(root, columns=("Block No", "Size", "Free", "Used", "Process"), show="headings")
        self.tree.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.update_memory_table()
        self.job_counter = 1

    def update_memory_table(self):
        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add updated rows
        for block in self.memory_blocks:
            process_display = ", ".join(f"{job} ({size}KB)" for job, size in block["Job Sizes"].items()) or "None"
            self.tree.insert("", "end", values=(
                block["Block No"], block["Size"], block["Free"], block["Used"], process_display
            ))

    def add_job(self):
        try:
            job_size = int(self.job_size_entry.get().strip())
        except ValueError:
            self.show_message("Job size must be a valid number!", "red")
            return

        # Auto-generate job name
        job_name = f"{self.job_counter}"
        self.job_counter += 1

        # Process the job using Next Fit Algorithm
        allocated = False
        start_pointer = self.allocation_pointer

        while True:
            block = self.memory_blocks[self.allocation_pointer]

            if block["Free"] >= job_size:
                # Allocate memory
                block["Free"] -= job_size
                block["Used"] += job_size
                block["Job Sizes"][job_name] = job_size
                allocated = True

                # Update allocation pointer
                self.allocation_pointer = (self.allocation_pointer + 1) % len(self.memory_blocks)
                break

            # Move to the next block
            self.allocation_pointer = (self.allocation_pointer + 1) % len(self.memory_blocks)
            if self.allocation_pointer == start_pointer:
                break

        if allocated:
            self.show_message(f"Job '{job_name}' of size {job_size} KB allocated successfully!", "green")
        else:
            self.show_message(f"Job '{job_name}' of size {job_size} KB could not be allocated.", "red")

        self.update_memory_table()

    def complete_job(self):
        complete =False
        job_name = self.job_name_entry.get().strip()
        if not job_name:
            self.show_message("Please enter a valid job name to complete.", "red")
            return

        for block in self.memory_blocks:
            if job_name in block["Job Sizes"]:
                job_size = block["Job Sizes"].pop(job_name)
                block["Free"] += job_size
                block["Used"] -= job_size
                complete = True

        if complete:
            self.show_message(f"Job '{job_name}' completed successfully!", "green")
            self.update_memory_table()
        else:
            self.show_message(f"Job '{job_name}' not found!", "red")

    def show_message(self, message, color):
        message_label = Label(self.root, text=message, fg=color)
        message_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.root.after(3000, message_label.destroy)


# Main application window
root = Tk()
app = NextFitMemoryAllocation(root)
root.mainloop()
