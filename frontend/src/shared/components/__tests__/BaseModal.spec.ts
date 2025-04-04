import { mount } from '@vue/test-utils';
import BaseModal from '../BaseModal.vue'; // Adjust path if necessary
import { nextTick } from 'vue'; // Import nextTick

describe('BaseModal.vue', () => {
  afterEach(() => {
    document.body.style.overflow = '';
    document.body.innerHTML = '';
  });

  it('does not render when modelValue is false', () => {
    const wrapper = mount(BaseModal, {
      props: { modelValue: false },
      slots: { default: 'Modal Content' },
      attachTo: document.body,
    });

    expect(wrapper.find('[role="dialog"]').exists()).toBe(false);

    expect(document.body.textContent).not.toContain('Modal Content');
    expect(document.body.style.overflow).toBe('');
  });

  it('renders correctly when modelValue is true', async () => {
    const wrapper = mount(BaseModal, {
      props: { modelValue: false },
      slots: { default: '<div data-testid="modal-content">Hello Modal</div>' },
      attachTo: document.body,
    });

    await wrapper.setProps({ modelValue: true });
    await nextTick();

    const modalElement = document.body.querySelector('[role="dialog"]');
    expect(modalElement).not.toBeNull();

    const contentElement = document.body.querySelector(
      '[data-testid="modal-content"]'
    );
    expect(contentElement).not.toBeNull();
    expect(contentElement?.textContent).toBe('Hello Modal');

    expect(
      document.body.querySelector('.fixed.inset-0 .bg-white.opacity-45')
    ).not.toBeNull(); // Overlay
    expect(modalElement?.classList.contains('bg-white')).toBe(true); // Modal background

    expect(document.body.style.overflow).toBe('hidden');

    await wrapper.setProps({ modelValue: false });
    await nextTick();
  });
});
