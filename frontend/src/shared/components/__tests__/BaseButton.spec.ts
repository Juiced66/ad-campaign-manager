import { mount } from '@vue/test-utils';
import BaseButton from '../BaseButton.vue';

describe('BaseButton.vue', () => {
  it('renders default button correctly with slot content', () => {
    const wrapper = mount(BaseButton, {
      slots: {
        default: 'Click Me',
      },
    });

    expect(wrapper.text()).toContain('Click Me');
    expect(wrapper.classes()).toContain('bg-indigo-600');
    expect(wrapper.classes()).toContain('px-3');
    expect(wrapper.find('svg').exists()).toBe(false);
    expect(wrapper.attributes('disabled')).toBeUndefined();
  });

  it('renders different button types', () => {
    const wrapperSubmit = mount(BaseButton, { props: { type: 'submit' } });
    expect(wrapperSubmit.attributes('type')).toBe('submit');

    const wrapperReset = mount(BaseButton, { props: { type: 'reset' } });
    expect(wrapperReset.attributes('type')).toBe('reset');
  });

  it('applies correct classes for variants', () => {
    const primary = mount(BaseButton, { props: { variant: 'primary' } });
    expect(primary.classes()).toContain('bg-indigo-600');
    expect(primary.classes()).toContain('text-white');

    const secondary = mount(BaseButton, { props: { variant: 'secondary' } });
    expect(secondary.classes()).toContain('bg-gray-100');
    expect(secondary.classes()).toContain('text-gray-800');
    expect(secondary.classes()).toContain('border-gray-300');

    const danger = mount(BaseButton, { props: { variant: 'danger' } });
    expect(danger.classes()).toContain('bg-red-600');
    expect(danger.classes()).toContain('text-white');

    const link = mount(BaseButton, { props: { variant: 'link' } });
    // Link variant might not have specific bg/text colors, check for absence of others
    expect(link.classes()).not.toContain('bg-indigo-600');
    expect(link.classes()).not.toContain('bg-gray-100');
    expect(link.classes()).not.toContain('bg-red-600');
  });

  it('applies correct classes for categories', () => {
    const defaultCat = mount(BaseButton, { props: { category: 'default' } });
    expect(defaultCat.classes()).toContain('px-3');
    expect(defaultCat.classes()).toContain('py-1.5');
    expect(defaultCat.classes()).toContain('rounded-md');

    const iconCat = mount(BaseButton, { props: { category: 'icon' } });
    expect(iconCat.classes()).toContain('p-1');
    expect(iconCat.classes()).toContain('rounded-full');
    expect(iconCat.classes()).toContain('w-8');
    expect(iconCat.classes()).toContain('h-8');

    const pillCat = mount(BaseButton, { props: { category: 'pill' } });
    expect(pillCat.classes()).toContain('px-3');
    expect(pillCat.classes()).toContain('py-1');
    expect(pillCat.classes()).toContain('rounded-full');
  });

  it('applies disabled attribute and styles when disabled prop is true', () => {
    const wrapper = mount(BaseButton, {
      props: { disabled: true },
      slots: { default: 'Cannot Click' },
    });

    expect(wrapper.attributes('disabled')).toBeDefined();
    expect(wrapper.classes()).toContain('opacity-50');
    expect(wrapper.classes()).toContain('cursor-not-allowed');
  });

  it('applies disabled attribute and styles when loading prop is true', () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true },
      slots: { default: 'Loading...' },
    });

    expect(wrapper.attributes('disabled')).toBeDefined();
    expect(wrapper.classes()).toContain('opacity-50');
    expect(wrapper.classes()).toContain('cursor-not-allowed');
  });

  it('shows loading spinner and retains slot content when loading prop is true', () => {
    // Note: The component currently adds the spinner alongside the slot, not replacing it.
    const wrapper = mount(BaseButton, {
      props: { loading: true },
      slots: { default: 'Processing' },
    });

    expect(wrapper.find('svg.animate-spin').exists()).toBe(true);
    expect(wrapper.text()).toContain('Processing'); // Slot content is still rendered
  });

  it('emits click event when clicked and not disabled/loading', async () => {
    const wrapper = mount(BaseButton);
    await wrapper.trigger('click');
    expect(wrapper.emitted()).toHaveProperty('click');
    expect(wrapper.emitted('click')).toHaveLength(1);
  });

  it('does not emit click event when disabled', async () => {
    const wrapper = mount(BaseButton, { props: { disabled: true } });
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toBeUndefined();
  });

  it('does not emit click event when loading', async () => {
    const wrapper = mount(BaseButton, { props: { loading: true } });
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toBeUndefined();
  });
});
