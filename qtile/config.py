
from typing import List  # noqa: F401

from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget import (CurrentLayout, GroupBox, Prompt, Spacer, WindowTab, Clock, QuickExit)

mod = "mod4"
terminal = "xfce4-terminal" 

def init_keys():
	keys = [
	# Switch between windows
	Key([mod], "left", lazy.layout.left()),
	Key([mod], "right", lazy.layout.right()),
	Key([mod], "down", lazy.layout.down()),
	Key([mod], "up", lazy.layout.up()),
	Key([mod], "space", lazy.layout.next()),

	# Move columns/stack
	Key([mod, "shift"], "left", lazy.layout.shuffle_left()),
	Key([mod, "shift"], "right", lazy.layout.shuffle_right()),
	Key([mod, "shift"], "down", lazy.layout.shuffle_down()),
	Key([mod, "shift"], "up", lazy.layout.shuffle_up()),

	# Grow windows.
	Key([mod, "control"], "left", lazy.layout.grow_left()),
	Key([mod, "control"], "right", lazy.layout.grow_right()),
	Key([mod, "control"], "down", lazy.layout.grow_down()),
	Key([mod, "control"], "up", lazy.layout.grow_up()),
	Key([mod], "n", lazy.layout.normalize()),
	
	# Toggle between split/unsplit
	Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
	Key([mod], "Return", lazy.spawn(terminal)),
	
	# Toggle etc.
	Key([mod], "Tab", lazy.next_layout()),
	Key([mod], "w", lazy.window.kill()),
	Key([mod, "control"], "r", lazy.restart()),
	Key([mod, "control"], "q", lazy.shutdown()),
	Key([mod], "r", lazy.spawncmd()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),
            desc="Switch to group {}".format(i.name),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    #layout.Columns(border_focus_stack=['#ff1268', '#ff1268'], border_width=1, margin=8),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    layout.MonadTall(border_focus=['#ff1268', '#ff1268'], border_width=1, margin=8),
    layout.MonadWide(border_focus=['#ff1268', '#ff1268'], border_width=1, margin=8),
    layout.Matrix(border_focus=['#ff1268', '#ff1268'], border_width=1, margin=4),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='source_code_pro_semibold',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
		widget.Spacer(length=800),
		widget.WindowTab(),
                widget.Clock(format='%m-%d-%Y %a %I:%M %p'),
                widget.QuickExit(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
