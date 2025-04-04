import { mount } from '@vue/test-utils';
import BaseSwitch from '../BaseSwitch.vue'; // Adjust path if necessary

describe('BaseSwitch.vue', () => {
  it('renders correctly in "off" state (modelValue = false)', () => {
    const wrapper = mount(BaseSwitch, {
      props: { modelValue: false },
    });

    const button = wrapper.find('button');
    const span = wrapper.find('span');

    // Check button background class for 'off' state
    expect(button.classes()).toContain('bg-gray-300');
    expect(button.classes()).not.toContain('bg-blue-600');

    // Check span transform class for 'off' state
    expect(span.classes()).toContain('translate-x-1');
    expect(span.classes()).not.toContain('translate-x-6');
  });

  it('renders correctly in "on" state (modelValue = true)', () => {
    const wrapper = mount(BaseSwitch, {
      props: { modelValue: true },
    });

    const button = wrapper.find('button');
    const span = wrapper.find('span');

    // Check button background class for 'on' state
    expect(button.classes()).toContain('bg-blue-600');
    expect(button.classes()).not.toContain('bg-gray-300');

    // Check span transform class for 'on' state
    expect(span.classes()).toContain('translate-x-6');
    expect(span.classes()).not.toContain('translate-x-1');
  });

  it('emits update:modelValue with true when clicked in "off" state', async () => {
    const wrapper = mount(BaseSwitch, {
      props: { modelValue: false },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.emitted('update:modelValue')).toHaveLength(1);
    expect(wrapper.emitted('update:modelValue')![0]).toEqual([true]);
  });

  it('emits update:modelValue with false when clicked in "on" state', async () => {
    const wrapper = mount(BaseSwitch, {
      props: { modelValue: true },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.emitted('update:modelValue')).toHaveLength(1);
    expect(wrapper.emitted('update:modelValue')![0]).toEqual([false]);
  });

  it('updates appearance when modelValue prop changes externally', async () => {
    const wrapper = mount(BaseSwitch, {
      props: { modelValue: false },
    });

    const button = wrapper.find('button');
    const span = wrapper.find('span');

    // Initial "off" state
    expect(button.classes()).toContain('bg-gray-300');
    expect(span.classes()).toContain('translate-x-1');

    // Change prop externally
    await wrapper.setProps({ modelValue: true });

    // Should now be in "on" state
    expect(button.classes()).toContain('bg-blue-600');
    expect(span.classes()).toContain('translate-x-6');

    // Change back externally
    await wrapper.setProps({ modelValue: false });

    // Should be back in "off" state
    expect(button.classes()).toContain('bg-gray-300');
    expect(span.classes()).toContain('translate-x-1');
  });
});
