import flet as ft
import requests
import html

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "TV Series Explorer"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1100
    page.window.height = 800
    page.padding = 35
    page.bgcolor = "#0F111A" 

    # --- UI Components ---
    results_grid = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=240,
        child_aspect_ratio=0.65, 
        spacing=25,
        run_spacing=25,
    )

    loader = ft.ProgressBar(visible=False, color="#E50914", bgcolor="#1A1C23")

    # --- Setup BottomSheet in Overlay ---
    details_sheet = ft.BottomSheet(content=ft.Container())
    page.overlay.append(details_sheet)

    def close_sheet(e):
        details_sheet.open = False
        page.update()

    # --- Logic: Display Show Details ---
    def show_details(show_data):
        summary = html.unescape(show_data.get('summary') or 'No description available.')
        summary_clean = summary.replace("<p>", "").replace("</p>", "").replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "")

        rating = (show_data.get('rating') or {}).get('average', 'N/A')
        image = (show_data.get('image') or {}).get('original', '')
        status = show_data.get('status', 'Unknown')
        premiered = show_data.get('premiered', 'Unknown Date')
        
        genre_badges = ft.Row(wrap=True, spacing=10)
        for genre in show_data.get('genres', []):
            genre_badges.controls.append(
                ft.Container(
                    content=ft.Text(genre, size=12, weight=ft.FontWeight.BOLD, color="white"),
                    # Modern padding method replacing deprecated symmetric()
                    padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
                    bgcolor="#2D303E",
                    border_radius=20
                )
            )

        details_sheet.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(show_data['name'], size=32, weight=ft.FontWeight.W_900),
                    ft.Container(content=ft.Text("✖", size=16, color="white70"), on_click=close_sheet, padding=10, ink=True, border_radius=50, bgcolor="#2D303E")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), # type: ignore
                
                ft.Divider(color="#2D303E", height=20),
                
                ft.Row([
                    ft.Container(
                        # Modern Flet method for Container background images
                        image=ft.DecorationImage(src=image, fit="cover") if image else None, # type: ignore
                        bgcolor="#1A1C23",
                        width=200,
                        height=300,
                        border_radius=12,
                        border=ft.Border.all(1, "#2D303E"),
                        shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color="#00000060", offset=ft.Offset(0, 5)),
                        content=ft.Text(" ", size=60) if not image else None,
                        alignment=ft.Alignment(0, 0)
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text(f"⭐ {rating}", size=20, color="#FFD700", weight=ft.FontWeight.BOLD),
                            ft.Text(f" •  {status}", size=16, color="#4ADE80" if status == "Running" else "white54", weight=ft.FontWeight.BOLD),
                            ft.Text(f" •  {premiered[:4]}", size=16, color="white54")
                        ]), # type: ignore
                        genre_badges,
                        ft.Container(height=10),
                        ft.Text("SYNOPSIS", size=14, weight=ft.FontWeight.BOLD, color="white54"),
                        ft.Text(summary_clean, size=15, color="white", weight=ft.FontWeight.W_400)
                    ], expand=True, spacing=10, alignment=ft.MainAxisAlignment.START) # type: ignore
                ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30) # type: ignore
            ], tight=True), # type: ignore
            padding=40,
            bgcolor="#11131C",
            border=ft.Border(top=ft.BorderSide(2, "#2D303E")),
            border_radius=ft.border_radius.only(top_left=25, top_right=25)
        )
        
        details_sheet.open = True
        page.update()

    # --- Logic: API Search ---
    def search_shows(e):
        query = search_input.value.strip()
        if not query:
            results_grid.controls.clear()
            page.update()
            return

        loader.visible = True
        page.update()

        try:
            response = requests.get(f"https://api.tvmaze.com/search/shows?q={query}")
            response.raise_for_status()
            data = response.json()

            results_grid.controls.clear()
            for item in data:
                show = item['show']
                
                # SAFETY: Using to prevent crashes from null API values
                poster = (show.get('image') or {}).get('medium', '')
                rating = (show.get('rating') or {}).get('average', 'N/A')
                network = (show.get('network') or show.get('webChannel') or {}).get('name', 'Web')
                
                show_card = ft.GestureDetector(
                    on_tap=lambda _, s=show: show_details(s),
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(
                                # Modern Flet method for Container background images
                                image=ft.DecorationImage(src=poster, fit="cover") if poster else None, # type: ignore
                                border_radius=8,
                                expand=True,
                                bgcolor="#11131C",
                                content=ft.Text(" ", size=40) if not poster else None,
                                alignment=ft.Alignment(0, 0)
                            ),
                            ft.Column([
                                ft.Text(show['name'], size=16, weight=ft.FontWeight.W_800, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row([
                                    ft.Text(f"⭐ {rating}", size=13, color="#FFD700", weight=ft.FontWeight.BOLD),
                                    ft.Text(network, size=12, color="white54", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True, text_align=ft.TextAlign.RIGHT)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) # type: ignore
                            ], spacing=2) # type: ignore
                        ], spacing=12), # type: ignore
                        padding=12,
                        bgcolor="#1A1C23",
                        border_radius=15,
                        border=ft.Border.all(1, "#2D303E"),
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="#00000040", offset=ft.Offset(0, 4)),
                        ink=True, 
                    )
                )
                results_grid.controls.append(show_card)

        except Exception as ex:
            # Log the exact error to the console for debugging and show a UI error
            print(f"Error during search: {ex}")
            results_grid.controls.append(ft.Text(f"Error: {ex}", color="#EF4444"))
        
        loader.visible = False
        page.update()

    # --- Search Bar UI ---
    search_input = ft.TextField(
        label="Search for TV Shows.",
        expand=True,
        border_radius=12,
        bgcolor="#1A1C23",
        border_color="#2D303E",
        focused_border_color="#E50914",
        prefix=ft.Text("  ", size=16),
        on_submit=search_shows 
    )

    search_btn = ft.Container(
        content=ft.Text("SEARCH", size=14, weight=ft.FontWeight.BOLD),
        # Modern padding method
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        bgcolor="#E50914",
        border_radius=12,
        ink=True,
        on_click=search_shows,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#E5091440")
    )

    # --- Page Assembly ---
    page.add(
        ft.Row([
            ft.Column([
                ft.Text("TV EXPLORER", size=36, weight=ft.FontWeight.W_900, color="#E50914"),
                ft.Text("Powered by TVmaze API", size=13, color="white", weight=ft.FontWeight.BOLD)
            ], spacing=2) # type: ignore
        ], alignment=ft.MainAxisAlignment.START), # type: ignore
        
        ft.Container(height=15),
        ft.Row([search_input, search_btn], spacing=15), # type: ignore
        loader,
        ft.Divider(color="#2D303E", height=30, thickness=1),
        results_grid
    )

if hasattr(ft, 'run'):
    ft.run(main)
else:
    ft.app(target=main)