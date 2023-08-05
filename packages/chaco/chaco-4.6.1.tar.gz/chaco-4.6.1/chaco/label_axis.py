""" Defines the LabelAxis class.
"""
# Major library imports
from traceback import print_exc
from numpy import array, float64, inf, searchsorted, take, unique

# Enthought library imports
from traits.api import Any, Str, List, Float

# Local, relative imports
from axis import PlotAxis
from label import Label


class LabelAxis(PlotAxis):
    """ An axis whose ticks are labeled with text instead of numbers.
    """

    # List of labels to use on tick marks.
    labels = List(Str)

    # The angle of rotation of the label. Only multiples of 90 are supported.
    label_rotation = Float(0)

    # List of indices of ticks
    positions = Any  # List(Float), Array

    def _compute_tick_positions(self, gc, component=None):
        """ Calculates the positions for the tick marks.

        Overrides PlotAxis.
        """
        if (self.mapper is None):
            self._reset_cache()
            self._cache_valid = True
            return

        datalow = self.mapper.range.low
        datahigh = self.mapper.range.high
        screenhigh = self.mapper.high_pos
        screenlow = self.mapper.low_pos

        if (datalow == datahigh) or (screenlow == screenhigh) or \
           (datalow in [inf, -inf]) or (datahigh in [inf, -inf]):
            self._reset_cache()
            self._cache_valid = True
            return

        if not self.tick_generator:
            return

        # Get a set of ticks from the tick generator.
        tick_list = array(self.tick_generator.get_ticks(datalow, datahigh,
                                                        datalow, datahigh,
                                                        self.tick_interval), float64)

        # Find all the positions in the current range.
        pos_index = []
        pos = []
        pos_min = None
        pos_max = None
        for i, position in enumerate(self.positions):
            if datalow <= position <= datahigh:
                pos_max = max(position, pos_max) if pos_max is not None else position
                pos_min = min(position, pos_min) if pos_min is not None else position
                pos_index.append(i)
                pos.append(position)
        if len(pos_index) == 0:
            # No positions currently visible.
            self._tick_positions = []
            self._tick_label_positions = []
            self._tick_label_list = []
            return

        # Use the ticks generated by the tick generator as a guide for selecting
        # the positions to be displayed.
        tick_indices = unique(searchsorted(pos, tick_list))
        tick_indices = tick_indices[tick_indices < len(pos)]
        tick_positions =  take(pos, tick_indices)
        self._tick_label_list = take(self.labels, take(pos_index, tick_indices))

        if datalow > datahigh:
            raise RuntimeError, "DataRange low is greater than high; unable to compute axis ticks."

        mapped_label_positions = [((self.mapper.map_screen(pos)-screenlow) / \
                                    (screenhigh-screenlow)) for pos in tick_positions]
        self._tick_positions = [self._axis_vector*tickpos + self._origin_point \
                                 for tickpos in mapped_label_positions]
        self._tick_label_positions = self._tick_positions
        return


    def _compute_labels(self, gc):
        """Generates the labels for tick marks.

        Overrides PlotAxis.
        """
        try:
            self.ticklabel_cache = []
            for text in self._tick_label_list:
                ticklabel = Label(text=text, font=self.tick_label_font,
                                  color=self.tick_label_color,
                                  rotate_angle=self.label_rotation)
                self.ticklabel_cache.append(ticklabel)

            self._tick_label_bounding_boxes = [array(ticklabel.get_bounding_box(gc), float64) for ticklabel in self.ticklabel_cache]
        except:
            print_exc()
        return

