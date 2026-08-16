"""Author DX re-exports. Ownership stays in ``ux_dom.ui``.

::

    from ux_app.ui import Button, Slider, ToastHost, Carousel

Install ux-dom to use this module. Application code still must not import
``ux_channel`` or ``cek_*`` — those stay behind ``ux_app.adapter``.
"""

from __future__ import annotations

try:
    from ux_dom.ui import (  # noqa: F401
        Alert,
        AlertDescription,
        AlertTitle,
        Avatar,
        AvatarFallback,
        AvatarImage,
        Badge,
        Button,
        Card,
        CardContent,
        CardDescription,
        CardFooter,
        CardHeader,
        CardTitle,
        Carousel,
        Chart,
        Checkbox,
        DatePicker,
        Dialog,
        Input,
        Label,
        Select,
        Separator,
        Skeleton,
        Slider,
        Switch,
        Table,
        TableBody,
        TableCaption,
        TableCell,
        TableEmpty,
        TableHead,
        TableHeader,
        TableRow,
        Tabs,
        Textarea,
        ToastHost,
        ToastItem,
        button_classes,
        cn,
        focus_ring,
        input_classes,
        radius,
        slider_classes,
        variants,
    )
    from ux_dom.ui.channel_bridge import (  # noqa: F401
        action_button_attrs,
        channel_available,
        live_button,
        public_form,
        stamp_region,
        to_fragment,
    )
except ImportError as exc:  # pragma: no cover - exercised when ux-dom absent
    raise ImportError(
        "ux_app.ui re-exports ux_dom.ui. Ownership of markup and tokens "
        "stays in ux-dom. Install: "
        "pip install 'ux-dom @ git+https://github.com/bitplorer/ux-dom.git'"
    ) from exc

__all__ = [
    "cn",
    "variants",
    "focus_ring",
    "radius",
    "Button",
    "button_classes",
    "Input",
    "input_classes",
    "Textarea",
    "Label",
    "Card",
    "CardHeader",
    "CardTitle",
    "CardDescription",
    "CardContent",
    "CardFooter",
    "Badge",
    "Alert",
    "AlertTitle",
    "AlertDescription",
    "Separator",
    "Skeleton",
    "Avatar",
    "AvatarImage",
    "AvatarFallback",
    "Checkbox",
    "Switch",
    "Select",
    "Slider",
    "slider_classes",
    "Table",
    "TableHeader",
    "TableBody",
    "TableRow",
    "TableHead",
    "TableCell",
    "TableCaption",
    "TableEmpty",
    "Tabs",
    "Dialog",
    "Carousel",
    "ToastHost",
    "ToastItem",
    "DatePicker",
    "Chart",
    "channel_available",
    "stamp_region",
    "action_button_attrs",
    "to_fragment",
    "live_button",
    "public_form",
]
