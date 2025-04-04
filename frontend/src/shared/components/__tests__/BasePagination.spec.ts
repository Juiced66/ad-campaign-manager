import { mount } from '@vue/test-utils';
import BasePagination from '../BasePagination.vue'; // Adjust path if necessary
import BaseButton from '../BaseButton.vue'; // BasePagination uses BaseButton

describe('BasePagination.vue', () => {
  const defaultProps = {
    page: 1,
    limit: 10,
    total: 100,
    disableNext: false,
  };

  it('renders limit dropdown, total count, current page, and buttons', () => {
    const wrapper = mount(BasePagination, {
      props: defaultProps,
    });

    // Limit Dropdown
    const select = wrapper.find('select#limit');
    expect(select.exists()).toBe(true);
    expect((select.element as HTMLSelectElement).value).toBe('10'); // Check initial limit

    // Total Count Display
    expect(wrapper.text()).toContain('Total : 100');

    // Current Page Display
    expect(wrapper.text()).toContain('Page 1');

    // Buttons (using component find)
    const buttons = wrapper.findAllComponents(BaseButton);
    expect(buttons).toHaveLength(2); // Prev and Next
    expect(buttons[0].text()).toBe('Prev');
    expect(buttons[1].text()).toBe('Next');
  });

  it('emits update:limit when limit dropdown changes', async () => {
    const wrapper = mount(BasePagination, {
      props: defaultProps,
    });

    const select = wrapper.find('select#limit');
    await select.setValue('25'); // Change value

    expect(wrapper.emitted('update:limit')).toHaveLength(1);
    expect(wrapper.emitted('update:limit')![0]).toEqual([25]); // Value should be a number
  });

  it('emits update:page with page - 1 when Prev button is clicked', async () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        page: 3, // Start on a page > 1
      },
    });

    const prevButton = wrapper.findAllComponents(BaseButton).at(0); // Find 'Prev' button
    await prevButton!.trigger('click');

    expect(wrapper.emitted('update:page')).toHaveLength(1);
    expect(wrapper.emitted('update:page')![0]).toEqual([2]); // page - 1
  });

  it('emits update:page with page + 1 when Next button is clicked', async () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        page: 3,
      },
    });

    const nextButton = wrapper.findAllComponents(BaseButton).at(1); // Find 'Next' button
    await nextButton!.trigger('click');

    expect(wrapper.emitted('update:page')).toHaveLength(1);
    expect(wrapper.emitted('update:page')![0]).toEqual([4]); // page + 1
  });

  it('"Prev" button is disabled when page is 1', () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        page: 1,
      },
    });

    const prevButton = wrapper.findAllComponents(BaseButton).at(0);
    // Check the disabled prop passed to BaseButton
    expect(prevButton!.props('disabled')).toBe(true);
    // Also check the attribute on the rendered button element
    expect(prevButton!.attributes('disabled')).toBeDefined();
  });

  it('"Prev" button is enabled when page is greater than 1', () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        page: 2,
      },
    });

    const prevButton = wrapper.findAllComponents(BaseButton).at(0);
    expect(prevButton!.props('disabled')).toBe(false);
    expect(prevButton!.attributes('disabled')).toBeUndefined();
  });

  it('"Next" button is disabled when disableNext prop is true', () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        disableNext: true,
      },
    });

    const nextButton = wrapper.findAllComponents(BaseButton).at(1);
    expect(nextButton!.props('disabled')).toBe(true);
    expect(nextButton!.attributes('disabled')).toBeDefined();
  });

  it('"Next" button is enabled when disableNext prop is false', () => {
    const wrapper = mount(BasePagination, {
      props: {
        ...defaultProps,
        disableNext: false,
      },
    });

    const nextButton = wrapper.findAllComponents(BaseButton).at(1);
    expect(nextButton!.props('disabled')).toBe(false);
    expect(nextButton!.attributes('disabled')).toBeUndefined();
  });

  it('updates displayed page number when page prop changes', async () => {
    const wrapper = mount(BasePagination, {
      props: defaultProps,
    });
    expect(wrapper.text()).toContain('Page 1');

    await wrapper.setProps({ page: 5 });

    expect(wrapper.text()).toContain('Page 5');
  });

  it('updates displayed total when total prop changes', async () => {
    const wrapper = mount(BasePagination, {
      props: defaultProps,
    });
    expect(wrapper.text()).toContain('Total : 100');

    await wrapper.setProps({ total: 42 });

    expect(wrapper.text()).toContain('Total : 42');
  });
});
