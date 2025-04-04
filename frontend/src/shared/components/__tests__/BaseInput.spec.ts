import { mount } from '@vue/test-utils';
import BaseInput from '../BaseInput.vue'; // Adjust path if necessary

describe('BaseInput.vue', () => {
  it('renders label when label prop is provided', () => {
    const labelText = 'Your Name';
    const wrapper = mount(BaseInput, {
      props: {
        label: labelText,
        id: 'name-input',
      },
    });

    const label = wrapper.find('label');
    expect(label.exists()).toBe(true);
    expect(label.text()).toBe(labelText);
    expect(label.attributes('for')).toBe('name-input');
  });

  it('does not render label when label prop is omitted', () => {
    const wrapper = mount(BaseInput);
    expect(wrapper.find('label').exists()).toBe(false);
  });

  it('renders input element', () => {
    const wrapper = mount(BaseInput);
    expect(wrapper.find('input').exists()).toBe(true);
  });

  it('binds v-model correctly', async () => {
    const wrapper = mount(BaseInput, {
      props: {
        modelValue: 'Initial Value',
        // Provide a function mock for the update event
        'onUpdate:modelValue': (e: string | number | null) =>
          wrapper.setProps({ modelValue: e }),
      },
    });

    const input = wrapper.find('input');

    // Check initial value
    expect((input.element as HTMLInputElement).value).toBe('Initial Value');

    // Simulate user input
    await input.setValue('New Value');

    // Check that the event was emitted (implicitly tested by the v-model update working)
    expect(wrapper.props('modelValue')).toBe('New Value');

    // Check if the update:modelValue event was emitted correctly (more explicit)
    expect(wrapper.emitted('update:modelValue')).toHaveLength(1);
    expect(wrapper.emitted('update:modelValue')![0]).toEqual(['New Value']);
  });

  it('sets the input type attribute correctly', () => {
    const textWrapper = mount(BaseInput, { props: { type: 'text' } });
    expect(textWrapper.find('input').attributes('type')).toBe('text');

    const passwordWrapper = mount(BaseInput, { props: { type: 'password' } });
    expect(passwordWrapper.find('input').attributes('type')).toBe('password');

    const dateWrapper = mount(BaseInput, { props: { type: 'date' } });
    expect(dateWrapper.find('input').attributes('type')).toBe('date');
  });

  it('displays error message when error prop is provided', () => {
    const errorText = 'This field is required';
    const wrapper = mount(BaseInput, {
      props: {
        error: errorText,
      },
    });

    const errorParagraph = wrapper.find('p.text-red-500');
    expect(errorParagraph.exists()).toBe(true);
    expect(errorParagraph.text()).toBe(errorText);
  });

  it('does not display error message when error prop is omitted', () => {
    const wrapper = mount(BaseInput);
    expect(wrapper.find('p.text-red-500').exists()).toBe(false);
  });

  it('associates label with input using id', () => {
    const inputId = 'user-email';
    const wrapper = mount(BaseInput, {
      props: {
        id: inputId,
        label: 'Email',
      },
    });

    expect(wrapper.find('label').attributes('for')).toBe(inputId);
    expect(wrapper.find('input').attributes('id')).toBe(inputId);
  });

  it('passes down other attributes ($attrs)', () => {
    const wrapper = mount(BaseInput, {
      attrs: {
        placeholder: 'Enter text here',
        disabled: true,
        'data-test': 'my-input',
      },
    });

    const input = wrapper.find('input');
    expect(input.attributes('placeholder')).toBe('Enter text here');
    expect(input.attributes('disabled')).toBeDefined();
    expect(input.attributes('data-test')).toBe('my-input');
  });

  it('applies disabled styles when disabled attribute is passed', () => {
    const wrapper = mount(BaseInput, {
      attrs: {
        disabled: true,
      },
    });
    expect(wrapper.find('input').classes()).toContain('disabled:opacity-50');
    // Note: Actual visual opacity testing is hard in unit tests, class check is usually sufficient
  });
});
