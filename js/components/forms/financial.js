import FormMixin from '../../mixins/form'
import optionsinput from '../options_input'
import textinput from '../text_input'

export default {
  name: 'financial',

  mixins: [FormMixin],

  components: {
    optionsinput,
    textinput,
  },

  props: {
    initialData: {
      type: Object,
      default: () => ({})
    }
  },

  data: function () {
    const {
      funding_type = ""
    } = this.initialData

    return {
      funding_type,
      shouldForceShowTaskOrder: false
    }
  },

  computed: {
    showTaskOrderUpload: function() {
      return !this.initialData.task_order.pdf || this.shouldForceShowTaskOrder
    }
  },

  methods: {
    forceShowTaskOrderUpload: function(e) {
      console.log("forceShowTaskOrder", e)
      e.preventDefault()
      this.shouldForceShowTaskOrder = true
    }
  }
}
