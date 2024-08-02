#!/usr/bin/env python
import click


@click.command()
@click.argument('fastqs', nargs=2, type=click.Path(exists=True))
@click.option('-o', '--output', default='concat.fastq', help='输出合并后的数据. (默认: concat.fastq)')
@click.help_option('-h', '--help')
def main(fastqs, output):
    """
    TCR PE150 没有 overlap 的双端 FASTQ 合并脚本.

    例子: python concat.py test_1.fq test_2.fq -o concat.fastq
    """
    input1, input2 = fastqs
    line_count = 0
    g = open(output, 'wt')

    with open(input1) as f1, open(input2) as f2:

        for line1, line2 in zip(f1, f2):
            line_count += 1

            # header 信息行
            if line_count % 4 == 1:
                head_info1 = line1.split(' ')[0]
                head_info2 = line2.split(' ')[0]

                if head_info1 != head_info2:
                    raise Exception(f'FASTQ当前序列不是一对. {head_info1} - {head_info2}')
                else:
                    g.write(head_info1 + '\n')

            # 序列行
            elif line_count % 4 == 2:
                g.write(f'{line1.strip()}{"X" * 100}{line2.strip()}\n')
            # +
            elif line_count % 4 == 3:
                g.write('+\n')
            # 质量行
            else:
                g.write(f'{line1.strip()}{"?" * 100}{line2.strip()}\n')

    g.close()


if __name__ == '__main__':
    main()
