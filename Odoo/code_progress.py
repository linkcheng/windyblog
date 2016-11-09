def write(self, cr, uid, ids, vals, context=None):
    if isinstance(ids, (int, long)):
        ids = [ids]

    start_date = vals.get('start_date', None)
    end_date = vals.get('end_date', None)
    today = datetime.now().strftime('%Y-%m-%d')

    for department_id in ids:
        department = self.browse(cr, uid, department_id, context=context)
        #ver3.0
        # 如果有效期止或者有效期始有变动
        if start_date or end_date:
            valid_start_date = start_date if start_date else department.start_date
            # end_date is False 时，表示数据清空，为无限期
            valid_end_date = end_date if (end_date or end_date is False) else department.end_date
            msg = None

            # 如果有效期止早于有效期始
            if valid_end_date and valid_end_date < valid_start_date:
                msg = _('The valid to date cannot be earlier than the valid from date.')

            # 如果 有效期止 是过去， 并且当前组织单元正在使用
            if (valid_end_date and valid_end_date < today) or (valid_start_date > today) and department.now_num > 0:
                value = _('There are employees assigned to this org unit so you cannot deactivate it. Please adjust accordingly.')
                if msg:
                    msg = value + '\n' + msg
                else:
                    msg = value

            if msg:
                raise ValidationError(msg)

            is_in_use = False
            # 如果今天过了或者是开始日期，表示该组织单元在使用
            if today >= valid_start_date:
                is_in_use = True

            # 如果今天已经过了截止日期，表示该组织单元过期，没有使用
            if valid_end_date and valid_end_date < today:
                is_in_use = False

            vals['is_in_use'] = is_in_use

        # ver2.0
        # 如果 有效期止 是过去
        if valid_end_date < today:
            value = None
            # 如果当前组织单元被员工正在使用
            if department.now_num > 0:
                value = _('There are employees assigned to this org unit so you cannot deactivate it. Please adjust accordingly.')
        
            # 如果有效期止早于有效期始
            if valid_end_date < valid_start_date:
                if value:
                    value += '\n'
                value += _('The valid to date cannot be earlier than the valid from date.')
        
            # 如果有违规，就提醒
            if value:
                raise ValidationError(value)

        # 如果 有效期止 是今天或者以后
        else:
            # 如果有效期止早于有效期始
            if valid_end_date < valid_start_date:
                raise ValidationError(
                    _('The valid to date cannot be earlier than the valid from date.'))

        # ver1.0
        # 如果 有效期止 是过去
        if valid_end_date < today:
            # 如果当前组织单元被员工正在使用
            if department.now_num > 0:
                # 如果有效期止早于有效期始
                if valid_end_date < valid_start_date:
                    raise ValidationError(
                        _('There are employees assigned to this org unit so you cannot deactivate it. Please adjust accordingly. \
\nThe valid to date cannot be earlier than the valid from date.'))
                    # 如果有效期止晚于或等于有效期始
                else:
                    raise ValidationError(
                        _('There are employees assigned to this org unit so you cannot deactivate it. Please adjust accordingly.'))
            # 如果当前组织单元没有被员工使用
            else:
                # 如果有效期止早于有效期始
                if valid_end_date < valid_start_date:
                    raise ValidationError(
                        _('The valid to date cannot be earlier than the valid from date.'))
        # 如果 有效期止 是今天或者以后
        else:
            # 如果有效期止早于有效期始
            if valid_end_date < valid_start_date:
                raise ValidationError(
                    _('The valid to date cannot be earlier than the valid from date.'))