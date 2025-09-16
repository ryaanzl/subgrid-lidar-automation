# main_las.py

from config import subgrid_list, error_log
from process import process_all_subgrids


def main():
    """Main entry point for LAS merging workflow."""
    process_all_subgrids(subgrid_list)

    if error_log:
        print("\nErrors encountered:")
        for err in error_log:
            print(f"- {err}")


if __name__ == "__main__":
    main()
