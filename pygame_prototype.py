import pygame

from game_archetypes import ARCHETYPES, DEFAULT_ARCHETYPE_KEY, get_archetype
from game_constants import FPS, HEIGHT, TECH_HEIGHT, TECH_WIDTH, WIDTH
from game_data import create_initial_regions
from game_models import GameState
from game_systems import execute_attack, start_research
from game_ui import render, render_tech_screen, summary_screen
from game_utils import load_font, load_map_surface
from game_tech import TECH_ORDER


def perform_attack(state: GameState) -> None:
    execute_attack(state)


def show_tech_screen(state: GameState, font: pygame.font.Font) -> None:
    screen = pygame.display.set_mode((TECH_WIDTH, TECH_HEIGHT))
    pygame.display.set_caption("黑客公司 - 科技树")
    clock = pygame.time.Clock()

    running = True
    while running and state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_t):
                    running = False
                    break
                if event.key == pygame.K_UP:
                    state.tech_selection_index = (
                        state.tech_selection_index - 1
                    ) % len(TECH_ORDER)
                elif event.key == pygame.K_DOWN:
                    state.tech_selection_index = (
                        state.tech_selection_index + 1
                    ) % len(TECH_ORDER)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tech_key = TECH_ORDER[state.tech_selection_index]
                    start_research(state, tech_key)

        if not running or not state.running:
            break

        render_tech_screen(screen, state, font)
        pygame.display.flip()
        clock.tick(FPS)

    if not state.running:
        return

    # Restore main window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("黑客公司")
    return screen


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("黑客公司")
    clock = pygame.time.Clock()
    font = load_font(20)

    background = load_map_surface()
    state = GameState(regions=create_initial_regions())
    state.archetype_key = DEFAULT_ARCHETYPE_KEY
    state.archetype_selection_index = 0
    state.selecting_archetype = True
    state.add_message("选择黑客身份：↑↓切换，回车确认。")

    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
                break

            if event.type == pygame.KEYDOWN:
                if state.selecting_archetype:
                    if event.key == pygame.K_ESCAPE:
                        state.running = False
                        break
                    elif event.key == pygame.K_UP:
                        state.archetype_selection_index = (
                            state.archetype_selection_index - 1
                        ) % len(ARCHETYPES)
                    elif event.key == pygame.K_DOWN:
                        state.archetype_selection_index = (
                            state.archetype_selection_index + 1
                        ) % len(ARCHETYPES)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected = ARCHETYPES[state.archetype_selection_index]
                        state.archetype_key = selected.key
                        state.selecting_archetype = False
                        state.add_message(f"当前身份：{selected.name} - {selected.description}")
                    continue

                if 1:#if state.tech_view:
                    if event.key in (pygame.K_ESCAPE, pygame.K_t):
                        state.tech_view = False
                        state.add_message("返回作战界面。")
                    elif event.key == pygame.K_UP:
                        state.tech_selection_index = (
                            state.tech_selection_index - 1
                        ) % len(TECH_ORDER)
                    elif event.key == pygame.K_DOWN:
                        state.tech_selection_index = (
                            state.tech_selection_index + 1
                        ) % len(TECH_ORDER)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        tech_key = TECH_ORDER[state.tech_selection_index]
                        start_research(state, tech_key)
                    continue

                if event.key == pygame.K_ESCAPE:
                    state.running = False
                    break
                if event.key == pygame.K_LEFT:
                    state.selected_index = (state.selected_index - 1) % len(state.regions)
                    state.selected_sector_index = 0
                elif event.key == pygame.K_RIGHT:
                    state.selected_index = (state.selected_index + 1) % len(state.regions)
                    state.selected_sector_index = 0
                elif event.key == pygame.K_UP:
                    region = state.regions[state.selected_index]
                    state.selected_sector_index = (state.selected_sector_index - 1) % len(region.sectors)
                elif event.key == pygame.K_DOWN:
                    region = state.regions[state.selected_index]
                    state.selected_sector_index = (state.selected_sector_index + 1) % len(region.sectors)
                elif event.key == pygame.K_SPACE:
                    perform_attack(state)
                elif event.key == pygame.K_t:
                    screen = show_tech_screen(state, font) or screen
                    if not state.running:
                        break
                    background = load_map_surface()

        render(screen, background, state, font)
        pygame.display.flip()
        clock.tick(FPS)

    if state.game_over:
        summary_screen(screen, state, font, clock, background)

    pygame.quit()


if __name__ == "__main__":
    main()

